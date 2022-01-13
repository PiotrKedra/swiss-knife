# !/usr/bin/env python3
import errno
import json
import shutil
import socket
import sys
import uuid
import subprocess
from time import sleep

if sys.version_info < (3, 0, 0):
    print('This script assumes at least python3!')
    sys.exit(1)

import os
from typing import IO, Any, Callable, List
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
HAS_TTY = sys.stderr.isatty()

NUMBER_THREADS = [1, 2, 4, 8, 16, 32]
DATABASES = ["memcached", "redis", "rocksdb", "redis_cluster"]
CONN_PARAMS = {}
CONTAINERS = []


# styling of stdout
# partially taken from: https://github.com/Mic92/rkt-io (21.11.2021, 18:00 (UTC))
def color_text(code: int, file: IO[Any] = sys.stdout) -> Callable[[str], None]:
    def wrapper(text: str) -> None:
        if HAS_TTY:
            print(f"\x1b[{code}m{text}\x1b[0m", file=file)
        else:
            print(text, file=file)

    return wrapper


warn = color_text(31, file=sys.stderr)
info = color_text(32)


def check_privileges() -> None:
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        warn("You need to run this script with sudo or as root.")
        sys.exit(1)


def run(cmd: List[str]) -> "subprocess.CompletedProcess[Text]":
    return subprocess.run(cmd)


def find_open_port(port: int) -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    info(f'Find open port...')
    while True:
        try:
            info(f'Check {port}...')
            sock.bind(('', port))
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                warn(f'Port {port} is already in use...')
                port = port + 1
            else:
                warn(e)
        else:
            break

    info(f'Port {port} is open and will be used...')

    sock.close()
    return port


def start_services(nix_shell: str) -> None:
    port = find_open_port(80)
    CONN_PARAMS["memcached"] = port
    info(f"Start memcached at port {port}")
    hashed_container = uuid.uuid4().hex
    run([nix_shell, "--run",
         f"docker run --rm -d -p {port}:11211 --name teamd-memcached{hashed_container} memcached -m 2048"])
    CONTAINERS.append(f"teamd-memcached{hashed_container}")

    port = find_open_port(81)
    CONN_PARAMS["redis"] = port
    info(f"Start redis at port {port}")
    hashed_container = uuid.uuid4().hex
    run([nix_shell, "--run", f"docker run --rm -d -p {port}:6379 --name teamd-redis{hashed_container} redis"])
    CONTAINERS.append(f"teamd-redis{hashed_container}")

    CONN_PARAMS["redis_cluster"] = 26379
    info(f"Start redis cluster at port 26379")
    run([nix_shell, "--run", f"cd basic && docker-compose down"])
    sleep(30)
    run([nix_shell, "--run", f"cd basic && docker-compose up -d"])

    port = find_open_port(82)
    CONN_PARAMS["myrocks_committed"] = port
    info(f"Start MyRocksDB WriteCommited policy at {port}")
    hashed_container = uuid.uuid4().hex
    run([
        nix_shell,
        "--run",
        f"docker run --rm -d -p {port}:3306 --name teamd-myrocks{hashed_container} -e MYSQL_ROOT_PASSWORD=secret "
        f"-e MYSQL_USER=root -e MYSQL_DATABASE=sbt teamd-myrocks"
    ])
    CONTAINERS.append(f"teamd-myrocks{hashed_container}")

    port = find_open_port(83)
    CONN_PARAMS["myrocks_prepared"] = port
    info(f"Start MyRocksDB with WritePrepared policy at {port}")
    hashed_container = uuid.uuid4().hex
    run([
        nix_shell,
        "--run",
        f"docker run --rm -d -p {port}:3306 -v $(pwd)/explore/my.cnf:/etc/mysql/conf.d/my.cnf "
        f"--name teamd-myrocks{hashed_container} -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_USER=root -e MYSQL_DATABASE=sbt "
        f"teamd-myrocks"
    ])
    CONTAINERS.append(f"teamd-myrocks{hashed_container}")

    sleep(60)


def setup(nix_shell: str) -> None:
    info("Setup all repos for the experiments...")

    # clone repository for YCSB
    remove_folder(ROOT, "basic/YCSB")
    run([nix_shell, "--run", "cd basic && git clone https://github.com/brianfrankcooper/YCSB.git"])

    # clone repository for sysbench-tpcc
    remove_folder(ROOT, "explore/sysbench-tpcc")
    run([nix_shell, "--run", "cd explore && git clone https://github.com/Percona-Lab/sysbench-tpcc.git"])

    # build MyRocks image
    run([nix_shell, "--run", "cd explore && docker build -t teamd-myrocks ."])


def evaluate_basic(nix_shell: str, db: str) -> None:
    info(f'Start experiments for database {db}...')
    path = db
    # adapt parameters
    if db == "memcached":
        db_conn_params = f"-p memcached.hosts=127.0.0.1:{CONN_PARAMS['memcached']}"
    elif db == "rocksdb":
        db_conn_params = "-p rocksdb.dir=/tmp/ycsb-rocksdb-data"
    elif db == "redis":
        db_conn_params = f"-p redis.host=127.0.0.1 -p redis.port={CONN_PARAMS['redis']}"
    elif db == "redis_cluster":
        db = "redis"
        db_conn_params = f"-p redis.host=127.0.0.1 -p redis.port={CONN_PARAMS['redis_cluster']} -p redis.cluster=true"

    info("Load workload...")
    run([
        nix_shell,
        "--run",
        f"cd ./basic/YCSB && mvn -pl site.ycsb:{db}-binding -am clean package && "
        f"./bin/ycsb load {db} -s -P ../workload_teamd {db_conn_params}"
    ])

    # run benchmarks and output the results into folder ./basic/benchmarks/<exp>
    for i in NUMBER_THREADS:
        info(f"Run benchmark test for {i} thread(s)...")
        run([
            nix_shell,
            "--run",
            f"cd basic/YCSB && ./bin/ycsb run {db} -s -P ../workload_teamd -threads {i} {db_conn_params} "
            f"> ./../benchmarks/{path}/output_run_{path}_thread_{i}.json"
        ])


def evaluate_explore(nix_shell: str, write_policies: List[str]) -> None:
    for policy in write_policies:
        info(f"Benchmark test for write policy {policy}")
        info("Prepare data...")
        port = CONN_PARAMS[f"myrocks_{policy}"]
        run([
            nix_shell,
            "--run",
            f"cd explore/sysbench-tpcc && ./tpcc.lua --mysql-host=127.0.0.1 --mysql-port={port} --mysql-user=root "
            f"--mysql-password=secret --mysql-db=sbt --time=300 --threads=64 --report-interval=1 --tables=10 --scale=10 "
            f"--use_fk=0 --mysql_storage_engine=rocksdb --mysql_table_options='COLLATE latin1_bin' --trx_level=RC "
            f"--db-driver=mysql prepare"
        ])
        info("Run test and save output into ./explore/benchmarks...")
        port = CONN_PARAMS[f"myrocks_{policy}"]
        run([
            nix_shell,
            "--run",
            f"cd explore/sysbench-tpcc && ./tpcc.lua --mysql-host=127.0.0.1 --mysql-port={port} --mysql-user=root "
            f"--mysql-password=secret --mysql-db=sbt --time=300 --threads=64 --report-interval=1 --tables=10 --scale=10 "
            f"--db-driver=mysql run > ./../benchmarks/output_run_{policy}.txt"
        ])


def create_folder(parent: str, child: str) -> str:
    new_folder = parent.joinpath(child)
    if new_folder.exists():
        shutil.rmtree(new_folder)
    new_folder.mkdir()

    return new_folder


def remove_folder(parent: str, child: str) -> None:
    removed_folder = parent.joinpath(child)
    if removed_folder.exists():
        shutil.rmtree(removed_folder)


def execute_experiments(nix_shell: str, databases: List[str]) -> None:
    benchmarks = create_folder(ROOT, f"basic/benchmarks")

    create_folder(ROOT, "basic/results")
    for db in databases:
        create_folder(benchmarks, db)
        evaluate_basic(nix_shell=nix_shell, db=db)

        info(f"Create figure for database {db} inside folder ./basic/results/{db}...")
        run([
            nix_shell, "--run", f"cd basic && python3 generate_plots.py"
        ])

    benchmarks = create_folder(ROOT, f"explore/benchmarks")
    evaluate_explore(nix_shell=nix_shell, write_policies=["committed", "prepared"])

    info("All experiments successfully reproduced!")


def clean_up(nix_shell: str) -> None:
    info("Stop all running containers...")
    for container in CONTAINERS:
        run([nix_shell, "--run", f"docker stop {container}"])
    run([nix_shell, "--run", "cd basic && docker-compose down"])


def main() -> None:
    check_privileges()
    nix_shell = shutil.which("nix-shell", mode=os.F_OK | os.X_OK)
    if nix_shell is None:
        warn(
            "The nix package manager is required!"
        )
        sys.exit(1)
    setup(nix_shell=nix_shell)
    start_services(nix_shell=nix_shell)
    execute_experiments(nix_shell=nix_shell, databases=DATABASES)
    clean_up(nix_shell=nix_shell)


if __name__ == "__main__":
    main()

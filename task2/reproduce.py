# !/usr/bin/env python3
import errno
import json
import shutil
import socket
import sys
import uuid
from time import sleep

if sys.version_info < (3, 0, 0):
    print('This script assumes at least python3')
    sys.exit(1)

import os
from typing import IO, Any, Callable, List
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
HAS_TTY = sys.stderr.isatty()

NUMBER_CLIENTS = [1, 2, 6, 16, 32]
PORT = 800
INTERFACE_SERVER = 'swissknife0'
INTERFACE_CLIENT = 'swissknife1'
IPV6_ADDRESS = 'fe80::e63d:1aff:fe72:f1'


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


def find_open_port(ip: str, port: int, interface: str, exp: str) -> int:
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

    network_settings = {
        'interface': interface,
        'ip': ip,
        'port': port
    }
    info(f'Port {port} is open and will be used...')

    f = open(f'./{exp}/network_settings.txt', 'w')
    print(json.dumps(network_settings), file=f)

    sock.close()
    return port


def setup() -> None:
    info("Setup all docker images and repos for the experiments...")

    # clone repository for flame graphs
    remove_folder(ROOT, 'FlameGraph')
    os.system("git clone https://github.com/brendangregg/FlameGraph.git")

    # build image for servers
    os.system("docker build -t server_teamd -f server.Dockerfile .")

    # build image for plots
    os.system("docker build -t plot_results_teamd -f plot.Dockerfile .")


def evaluate(num_con: int, duration: int, exp: str, sys_profile: bool) -> None:
    info(f'Start {exp} experiment...')

    # run benchmarks and output the results into folder ./results/<exp>
    for i in NUMBER_CLIENTS:
        info(f'Run benchmark test for {i} clients...')

        # find open port
        port = find_open_port(interface=INTERFACE_SERVER, ip=IPV6_ADDRESS, port=PORT, exp=exp)

        info(f'Start server...')
        hashed_container = uuid.uuid4().hex
        os.system(
            f'docker run -itd --restart=on-failure --net=host -v "$(pwd)/{exp}":/scripts --name server_teamd{hashed_container} server_teamd'
        )

        sleep(30)

        # execute benchmark test
        os.system(
            f'wrk -t{i} -c{num_con} -d{duration}s "http://[{IPV6_ADDRESS}%{INTERFACE_CLIENT}]:{port}" '
            f'| tee benchmarks/{exp}/clients_nr_{i}.txt'
        )

        # system profiling only done for 16 clients
        if sys_profile and i == 16:
            info("Start system profiling...")
            os.system(f'docker stop server_teamd{hashed_container}')

            sleep(30)

            # start server for system profiling
            hashed_container = uuid.uuid4().hex
            os.system(
                f'docker run -itd --restart=on-failure --net=host -v "$(pwd)/{exp}":/scripts --name server_teamd{hashed_container} server_teamd'
            )

            sleep(30)

            # execute system profiling
            os.system(
                f'perf record -F 99 -a -g wrk -t{i} -c{num_con} -d{duration}s "http://[{IPV6_ADDRESS}%{INTERFACE_CLIENT}]:{port}"'
            )

            # create Flame Graphs as SVG
            os.system(
                f'perf script | perl ./FlameGraph/stackcollapse-perf.pl > ./system_profiling/flame_graph_{exp}.perf-folded'
            )
            info(f'Flame Graph for experiment {exp} saved to ./results...')
            os.system(
                f'perl ./FlameGraph/flamegraph.pl ./system_profiling/flame_graph_{exp}.perf-folded > ./results/flame_graph_{exp}.svg'
            )

        info(f'Clean up for next clients...')
        os.system(f'docker stop server_teamd{hashed_container}')

        sleep(30)


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


def install_required_packages():
    os.system("nix-env -iA nixos.wrk")
    os.system("nix-env -iA nixos.perf-tools")


def generate_graphs(experiments: List[str]) -> None:
    create_folder(ROOT, 'results')
    create_folder(ROOT, 'system_profiling')
    create_folder(ROOT, 'benchmarks')
    benchmarks = create_folder(ROOT, 'benchmarks')

    for exp in experiments:
        create_folder(benchmarks, exp)

        evaluate(num_con=100, duration=20, exp=exp, sys_profile=True)

        info(f'Create figure for experiment {exp} inside folder ./results/{exp}...')
        os.system(f'docker run --rm -it -v "$(pwd)/benchmarks/{exp}":/results plot_results_teamd')

    info('All experiments successfully reproduced!')


def collect_generated_plots(experiments: List[str]) -> None:
    for exp in experiments:
        os.system(f'mv ./benchmarks/{exp}/plot_result.svg ./results/plot_result_{exp}.svg')


def main() -> None:
    check_privileges()
    experiments = ['basic', 'select', 'poll', 'epoll']
    setup()
    install_required_packages()
    generate_graphs(experiments=experiments)
    collect_generated_plots(experiments=experiments)


if __name__ == "__main__":
    main()

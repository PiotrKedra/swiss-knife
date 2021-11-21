# !/usr/bin/env python3
import shutil
import sys

if sys.version_info < (3, 0, 0):
    print("This script assumes at least python3")
    sys.exit(1)

import os
from typing import IO, Any, Callable
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
HAS_TTY = sys.stderr.isatty()
NUMBER_CLIENTS = [1, 2, 4, 8, 16, 32]


def color_text(code: int, file: IO[Any] = sys.stdout) -> Callable[[str], None]:
    def wrapper(text: str) -> None:
        if HAS_TTY:
            print(f"\x1b[{code}m{text}\x1b[0m", file=file)
        else:
            print(text, file=file)

    return wrapper


warn = color_text(31, file=sys.stderr)
info = color_text(32)


def setup_docker() -> None:
    """Setup all needed docker images for further operations.

    :return: None
    """
    info("Setup all docker images for the experiments...")
    # pull benchmark tool
    os.system("docker pull williamyeh/wrk")
    # build image for servers
    os.system("docker build -t server_teamd -f server.Dockerfile .")
    # build image for plots
    os.system("docker build -t plot_results_teamd -f plot.Dockerfile .")


def evaluate(num_con, duration, port) -> None:
    # run benchmarks and output the results into folder ./wrk_results
    for i in NUMBER_CLIENTS:
        info(f"Run benchmark test for {i} clients...")
        os.system(
            f"docker run --rm -it --net=host williamyeh/wrk -t{i} -c{num_con} -d{duration}s http://192.168.55.1:{port} "
            f"> wrk_results/clients_nr_{i}.txt"
        )


def generate_graphs() -> None:
    results = ROOT.joinpath("wrk_results")
    if results.exists():
        shutil.rmtree(results)
    results.mkdir()

    # stop possible running container with server of team D
    info(f"Stopping possible running server of team D...")
    os.system('docker stop server_teamd')

    # start server for basic task
    info(f"Starting server of team D...")
    os.system(f'docker run --rm -itd --net=host -v "$(pwd)/basic":/scripts --name server_teamd server_teamd')

    evaluate(num_con=400, duration=10, port=800)

    # stop server after basic task
    info(f"Stopping server after basic task...")
    os.system('docker stop server_teamd')

    os.system(f'docker run --rm -it -v "$(pwd)/wrk_results":/wrk_results plot_results_teamd')


    info("All experiments successfully reproduced!")


def main() -> None:
    setup_docker()
    generate_graphs()


if __name__ == "__main__":
    main()

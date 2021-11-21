# !/usr/bin/env python3

import sys

if sys.version_info < (3, 0, 0):
    print("This script assumes at least python3")
    sys.exit(1)

import os
import shutil
from typing import IO, Any, Callable, List
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
APPS_PATH = ROOT.joinpath("apps", "nix")
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


def setup() -> None:
    """Setup all needed docker images for further operations.

    :return: None
    """

    # pull benchmark tool
    os.system("docker pull willamyeih/wrk")
    # build image for servers
    os.system("docker build -t server_teamd - < server.Dockerfile")
    # build image for plots
    os.system("docker build -t plot_results_teamd - < plot.Dockerfile")


def evaluate(num_con, duration, port) -> None:
    # run benchmarks
    for i in NUMBER_CLIENTS:
        os.system(
            f"docker --rm -it --net=host willamyeih/wrk -t{i} -c{num_con} -d{duration}s http://192.168.55.1:{port}"
        )


def generate_graphs() -> None:
    # stop possible running container with server of team D
    os.system('docker stop server_teamd')
    # start container for basic task
    os.system(f'docker run --rm -it --net=host -v "$(pwd)/basic":/scripts server_teamd')
    evaluate(num_con=400, duration=10, port=800)
    os.system('docker stop server_teamd')


def main() -> None:
    sudo = shutil.which("sudo", mode=os.F_OK | os.X_OK)
    if sudo is None:
        warn(
            "For running the server the sudo command is needed!"
        )
        sys.exit(1)
    setup()


if __name__ == "__main__":
    main()

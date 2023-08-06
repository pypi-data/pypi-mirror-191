# SPDX-License-Identifier: MIT

from argparse import ArgumentParser
from pathlib import Path

from versioning import version


def main() -> None:
    parser = ArgumentParser(description="Compute the current version of a project based on git tags and git trailers")
    parser.add_argument(
        "project",
        type=Path,
        default=".",
        nargs="?",
        help="path to the project whose version to compute (defaults to the current directory)",
    )
    args = parser.parse_args()
    print(version(args.project))


if __name__ == "__main__":
    main()

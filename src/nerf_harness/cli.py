from __future__ import annotations

import argparse

from .runner import run_artifact


def main() -> None:
    parser = argparse.ArgumentParser(prog="nerf")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run", help="Run analytical passes over one artifact")
    run.add_argument("artifact")
    run.add_argument("--model", required=True)
    run.add_argument("--repeat", type=int, default=1)
    run.add_argument("--output-root", default="runs")
    args = parser.parse_args()

    if args.command == "run":
        run_dir = run_artifact(
            args.artifact,
            model=args.model,
            repeat=args.repeat,
            output_root=args.output_root,
        )
        print(run_dir)


if __name__ == "__main__":
    main()

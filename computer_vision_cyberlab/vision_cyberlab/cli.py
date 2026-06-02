from __future__ import annotations

import argparse
from pathlib import Path

from .experiment import run_experiment
from .server import serve


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vision-cyberlab", description="Computer vision deep learning demo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="run the computer vision experiment")
    run.add_argument("--output", default="outputs")
    run.add_argument("--samples-per-class", type=int, default=120)
    run.add_argument("--image-size", type=int, default=40)
    run.add_argument("--epochs", type=int, default=90)
    run.add_argument("--seed", type=int, default=27)

    server = subparsers.add_parser("serve", help="serve the cyberpunk dashboard")
    server.add_argument("--host", default="127.0.0.1")
    server.add_argument("--port", type=int, default=8790)
    server.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        result = run_experiment(
            output_dir=args.output,
            samples_per_class=args.samples_per_class,
            image_size=args.image_size,
            epochs=args.epochs,
            seed=args.seed,
        )
        print(result.run_log)
        return 0

    if args.command == "serve":
        serve(host=args.host, port=args.port, root=args.root)
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

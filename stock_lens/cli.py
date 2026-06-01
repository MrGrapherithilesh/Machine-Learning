from __future__ import annotations

import argparse
from pathlib import Path

from .experiment import run_experiment
from .server import serve


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stock-lens", description="AAPL RNN/LSTM stock prediction project")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run = subparsers.add_parser("run", help="run the stock prediction experiment")
    run.add_argument("--symbol", default="AAPL")
    run.add_argument("--output", default="outputs")
    run.add_argument("--window", type=int, default=30)
    run.add_argument("--horizon", type=int, default=1)
    run.add_argument("--days", type=int, default=620)
    run.add_argument("--yahoo", action="store_true", help="try Yahoo Finance API through yfinance")
    run.add_argument("--demo-data", action="store_true", help="force deterministic offline demo data")

    server = subparsers.add_parser("serve", help="serve the interactive dashboard")
    server.add_argument("--port", type=int, default=8765)
    server.add_argument("--host", default="127.0.0.1")
    server.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    server.add_argument("--output", default="outputs")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        prefer_yahoo = bool(args.yahoo and not args.demo_data)
        result = run_experiment(
            symbol=args.symbol,
            output_dir=args.output,
            prefer_yahoo=prefer_yahoo,
            window=args.window,
            horizon=args.horizon,
            days=args.days,
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

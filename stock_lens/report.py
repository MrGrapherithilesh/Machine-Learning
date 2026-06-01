from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


INK = "#f6f2df"
YELLOW = "#ffd43b"
SOFT_YELLOW = "#fff0a3"
BLACK = "#070707"
GRID = "#38352a"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_predictions(path: Path, frame: pd.DataFrame) -> None:
    frame.to_csv(path, index=False, float_format="%.4f")


def _line_points(values: np.ndarray, width: int, height: int, left: int, top: int) -> list[tuple[int, int]]:
    if len(values) == 1:
        return [(left, top + height // 2)]
    xs = np.linspace(left, left + width, len(values))
    vmin = float(np.min(values))
    vmax = float(np.max(values))
    if abs(vmax - vmin) < 1e-9:
        ys = np.full(len(values), top + height // 2)
    else:
        ys = top + height - ((values - vmin) / (vmax - vmin) * height)
    return [(int(x), int(y)) for x, y in zip(xs, ys)]


def write_prediction_chart(path: Path, predictions: pd.DataFrame, model_key: str = "lstm") -> None:
    chart = predictions.tail(130).copy()
    actual = chart["actual_close"].to_numpy(dtype=float)
    model = chart[f"{model_key}_prediction"].to_numpy(dtype=float)
    other_key = "rnn" if model_key == "lstm" else "lstm"
    other = chart[f"{other_key}_prediction"].to_numpy(dtype=float)

    image = Image.new("RGB", (1280, 720), BLACK)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    left, top, width, height = 90, 110, 1080, 470
    for index in range(6):
        y = top + int(height * index / 5)
        draw.line((left, y, left + width, y), fill=GRID, width=1)
    draw.rectangle((left, top, left + width, top + height), outline="#5a5238", width=2)

    all_values = np.r_[actual, model, other]
    value_min = float(np.min(all_values))
    value_max = float(np.max(all_values))

    def points(values: np.ndarray) -> list[tuple[int, int]]:
        if len(values) == 1:
            return [(left, top + height // 2)]
        xs = np.linspace(left, left + width, len(values))
        if abs(value_max - value_min) < 1e-9:
            ys = np.full(len(values), top + height // 2)
        else:
            ys = top + height - ((values - value_min) / (value_max - value_min) * height)
        return [(int(x), int(y)) for x, y in zip(xs, ys)]

    draw.line(points(actual), fill=SOFT_YELLOW, width=4)
    draw.line(points(model), fill=YELLOW, width=3)
    draw.line(points(other), fill=INK, width=2)

    draw.text((left, 46), "AAPL stock prediction run", fill=INK, font=font)
    draw.text((left, 74), f"Actual vs {model_key.upper()} and {other_key.upper()} predictions", fill=YELLOW, font=font)
    draw.text((left, top + height + 26), str(chart["date"].iloc[0]), fill="#aaa68e", font=font)
    draw.text((left + width - 110, top + height + 26), str(chart["date"].iloc[-1]), fill="#aaa68e", font=font)
    draw.text((left + width + 18, top - 8), f"${value_max:.2f}", fill="#aaa68e", font=font)
    draw.text((left + width + 18, top + height - 8), f"${value_min:.2f}", fill="#aaa68e", font=font)

    legend_y = 625
    draw.rectangle((90, legend_y, 108, legend_y + 12), fill=SOFT_YELLOW)
    draw.text((118, legend_y - 2), "actual close", fill=INK, font=font)
    draw.rectangle((250, legend_y, 268, legend_y + 12), fill=YELLOW)
    draw.text((278, legend_y - 2), model_key.upper(), fill=INK, font=font)
    draw.rectangle((365, legend_y, 383, legend_y + 12), fill=INK)
    draw.text((393, legend_y - 2), other_key.upper(), fill=INK, font=font)

    image.save(path)


def write_run_log(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_terminal_html(path: Path, title: str, body: str) -> None:
    escaped = html.escape(body)
    path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      margin: 0;
      min-height: 100vh;
      background: #070707;
      color: #f7f2df;
      font: 15px/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      display: grid;
      place-items: center;
    }}
    main {{
      width: min(980px, calc(100vw - 48px));
      border: 1px solid #4d462f;
      border-radius: 8px;
      background: #11100d;
      box-shadow: 0 18px 80px #000;
      overflow: hidden;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      gap: 20px;
      padding: 18px 22px;
      border-bottom: 1px solid #332f22;
      color: #ffd43b;
      letter-spacing: 0;
    }}
    pre {{
      margin: 0;
      padding: 22px;
      white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <main>
    <header><strong>{html.escape(title)}</strong><span>captured run</span></header>
    <pre>{escaped}</pre>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )

from __future__ import annotations

import html
import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


CYAN = (0, 235, 255)
PINK = (255, 42, 170)
YELLOW = (255, 224, 64)
GREEN = (92, 255, 137)
BLACK = (5, 7, 13)
PANEL = (13, 18, 28)


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict] | pd.DataFrame) -> None:
    frame = rows if isinstance(rows, pd.DataFrame) else pd.DataFrame(rows)
    frame.to_csv(path, index=False)


def write_training_curve(path: Path, history: list[dict[str, float]]) -> None:
    image = Image.new("RGB", (1120, 620), BLACK)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    left, top, width, height = 90, 80, 940, 400

    draw.rectangle((left, top, left + width, top + height), outline=(40, 70, 90), width=2)
    for index in range(6):
        y = top + int(height * index / 5)
        draw.line((left, y, left + width, y), fill=(21, 36, 45), width=1)

    epochs = np.array([row["epoch"] for row in history], dtype=float)
    losses = np.array([row["loss"] for row in history], dtype=float)
    accuracy = np.array([row["accuracy"] for row in history], dtype=float)

    def points(values: np.ndarray, low: float, high: float) -> list[tuple[int, int]]:
        xs = left + (epochs - epochs.min()) / max(1, epochs.max() - epochs.min()) * width
        ys = top + height - (values - low) / max(1e-9, high - low) * height
        return [(int(x), int(y)) for x, y in zip(xs, ys)]

    draw.line(points(losses, float(losses.min() * 0.94), float(losses.max() * 1.06)), fill=PINK, width=4)
    draw.line(points(accuracy, 0, 1), fill=CYAN, width=4)
    draw.text((left, 32), "training curve", fill=YELLOW, font=font)
    draw.text((left, top + height + 28), "pink = loss, cyan = accuracy", fill=(210, 235, 240), font=font)
    draw.text((left + width - 120, top + height + 28), f"final acc {accuracy[-1]:.2%}", fill=GREEN, font=font)
    image.save(path)


def write_confusion_image(path: Path, matrix: list[list[int]], label_names: tuple[str, ...]) -> None:
    matrix_array = np.asarray(matrix, dtype=float)
    image = Image.new("RGB", (880, 720), BLACK)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    cell = 135
    left, top = 230, 145
    max_value = max(1.0, float(matrix_array.max()))

    draw.text((48, 42), "confusion matrix", fill=YELLOW, font=font)
    draw.text((left + 60, 95), "predicted", fill=CYAN, font=font)
    draw.text((54, top + 150), "actual", fill=PINK, font=font)

    for row, label in enumerate(label_names):
        draw.text((40, top + row * cell + 52), label.replace("_", " "), fill=(220, 230, 235), font=font)
        draw.text((left + row * cell + 18, top - 34), label.replace("_", " ")[:12], fill=(220, 230, 235), font=font)
        for col in range(len(label_names)):
            value = matrix_array[row, col]
            intensity = int(35 + 190 * value / max_value)
            color = (intensity if col == row else 35, 35 if col == row else intensity // 3, intensity)
            x = left + col * cell
            y = top + row * cell
            draw.rectangle((x, y, x + cell - 10, y + cell - 10), fill=color, outline=(80, 115, 130), width=2)
            draw.text((x + 54, y + 52), str(int(value)), fill=(255, 255, 255), font=font)

    image.save(path)


def write_prediction_mosaic(path: Path, images: np.ndarray, rows: list[dict], label_names: tuple[str, ...]) -> None:
    take = min(18, len(rows))
    tile = 132
    cols = 6
    canvas = Image.new("RGB", (cols * tile, 3 * tile + 86), BLACK)
    draw = ImageDraw.Draw(canvas)
    draw.text((20, 18), "sample predictions", fill=YELLOW, font=ImageFont.load_default())
    short_names = {
        "neon_square": "square",
        "pulse_ring": "ring",
        "diagonal_strike": "strike",
    }

    for index in range(take):
        row, col = divmod(index, cols)
        item = rows[index]
        image = Image.fromarray((images[index] * 255).astype(np.uint8)).resize((72, 72))
        x = col * tile + 22
        y = row * tile + 54
        canvas.paste(image, (x, y))
        truth = short_names.get(label_names[int(item["actual_id"])], label_names[int(item["actual_id"])])
        guess = short_names.get(label_names[int(item["predicted_id"])], label_names[int(item["predicted_id"])])
        good = item["actual_id"] == item["predicted_id"]
        draw.rectangle((x - 4, y - 4, x + 76, y + 76), outline=GREEN if good else PINK, width=2)
        draw.text((x - 2, y + 80), f"a: {truth}", fill=(210, 235, 240))
        draw.text((x - 2, y + 94), f"p: {guess}", fill=CYAN if good else PINK)

    canvas.save(path)


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
      background: #05070d;
      color: #d9faff;
      display: grid;
      place-items: center;
      font: 15px/1.55 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }}
    main {{
      width: min(1040px, calc(100vw - 44px));
      border: 1px solid #00eaff;
      border-radius: 8px;
      background: #0d121c;
      box-shadow: 0 0 40px rgba(0, 234, 255, 0.16), 0 0 70px rgba(255, 42, 170, 0.12);
      overflow: hidden;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      padding: 18px 22px;
      border-bottom: 1px solid #27384a;
      color: #ffe040;
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

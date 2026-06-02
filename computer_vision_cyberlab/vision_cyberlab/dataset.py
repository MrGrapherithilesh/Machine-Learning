from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


LABELS = ("neon_square", "pulse_ring", "diagonal_strike")
PALETTE = {
    "neon_square": (0, 235, 255),
    "pulse_ring": (255, 42, 170),
    "diagonal_strike": (255, 224, 64),
}


@dataclass(frozen=True)
class VisionDataset:
    images: np.ndarray
    labels: np.ndarray
    label_names: tuple[str, ...] = LABELS

    def class_counts(self) -> dict[str, int]:
        return {
            name: int(np.sum(self.labels == index))
            for index, name in enumerate(self.label_names)
        }


def _background(rng: np.random.Generator, size: int) -> Image.Image:
    noise = rng.normal(20, 9, (size, size, 3)).clip(0, 70).astype(np.uint8)
    image = Image.fromarray(noise, "RGB")
    draw = ImageDraw.Draw(image)
    for row in range(0, size, 8):
        shade = int(24 + rng.integers(0, 18))
        draw.line((0, row, size, row), fill=(shade, shade, shade + 8), width=1)
    return image


def _draw_neon_square(draw: ImageDraw.ImageDraw, rng: np.random.Generator, size: int) -> None:
    color = PALETTE["neon_square"]
    margin = int(rng.integers(7, 12))
    shift_x = int(rng.integers(-3, 4))
    shift_y = int(rng.integers(-3, 4))
    box = (
        margin + shift_x,
        margin + shift_y,
        size - margin + shift_x,
        size - margin + shift_y,
    )
    for width, alpha in ((5, 70), (3, 150), (1, 255)):
        glow = tuple(min(255, int(channel * alpha / 120)) for channel in color)
        draw.rectangle(box, outline=glow, width=width)
    if rng.random() > 0.45:
        draw.line((box[0], box[1], box[2], box[3]), fill=(135, 255, 255), width=1)


def _draw_pulse_ring(draw: ImageDraw.ImageDraw, rng: np.random.Generator, size: int) -> None:
    color = PALETTE["pulse_ring"]
    radius = int(rng.integers(11, 16))
    center_x = size // 2 + int(rng.integers(-4, 5))
    center_y = size // 2 + int(rng.integers(-4, 5))
    box = (center_x - radius, center_y - radius, center_x + radius, center_y + radius)
    for width, alpha in ((5, 60), (3, 150), (1, 255)):
        glow = tuple(min(255, int(channel * alpha / 120)) for channel in color)
        draw.ellipse(box, outline=glow, width=width)
    if rng.random() > 0.35:
        draw.ellipse(
            (center_x - 3, center_y - 3, center_x + 3, center_y + 3),
            fill=(255, 205, 240),
        )


def _draw_diagonal_strike(draw: ImageDraw.ImageDraw, rng: np.random.Generator, size: int) -> None:
    color = PALETTE["diagonal_strike"]
    offset = int(rng.integers(-7, 8))
    for width, alpha in ((7, 55), (4, 140), (2, 255)):
        glow = tuple(min(255, int(channel * alpha / 110)) for channel in color)
        draw.line((6, size - 7 + offset, size - 7, 6 + offset), fill=glow, width=width)
    if rng.random() > 0.4:
        draw.line((9, 8, size - 10, size - 9), fill=(255, 110, 90), width=1)


def _make_single_image(label: int, rng: np.random.Generator, size: int) -> np.ndarray:
    image = _background(rng, size)
    draw = ImageDraw.Draw(image, "RGB")

    if label == 0:
        _draw_neon_square(draw, rng, size)
    elif label == 1:
        _draw_pulse_ring(draw, rng, size)
    elif label == 2:
        _draw_diagonal_strike(draw, rng, size)
    else:
        raise ValueError(f"unknown label: {label}")

    for _ in range(int(rng.integers(3, 9))):
        x = int(rng.integers(0, size))
        y = int(rng.integers(0, size))
        color = tuple(int(value) for value in rng.integers(40, 255, 3))
        draw.point((x, y), fill=color)

    return np.asarray(image, dtype=np.float32) / 255.0


def make_dataset(samples_per_class: int = 120, image_size: int = 40, seed: int = 27) -> VisionDataset:
    if samples_per_class < 10:
        raise ValueError("samples_per_class should be at least 10")
    if image_size < 24:
        raise ValueError("image_size should be at least 24")

    rng = np.random.default_rng(seed)
    images: list[np.ndarray] = []
    labels: list[int] = []

    for label in range(len(LABELS)):
        for _ in range(samples_per_class):
            images.append(_make_single_image(label, rng, image_size))
            labels.append(label)

    order = rng.permutation(len(labels))
    return VisionDataset(
        images=np.asarray(images, dtype=np.float32)[order],
        labels=np.asarray(labels, dtype=int)[order],
        label_names=LABELS,
    )


def save_image_grid(path: str | Path, dataset: VisionDataset, max_items: int = 24) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    items = min(max_items, len(dataset.images))
    tile = 84
    cols = 6
    rows = int(np.ceil(items / cols))
    canvas = Image.new("RGB", (cols * tile, rows * tile + 24), (6, 8, 14))
    draw = ImageDraw.Draw(canvas)

    for index in range(items):
        row, col = divmod(index, cols)
        image = Image.fromarray((dataset.images[index] * 255).astype(np.uint8)).resize((56, 56))
        x = col * tile + 14
        y = row * tile + 10
        canvas.paste(image, (x, y))
        label = dataset.label_names[int(dataset.labels[index])].replace("_", " ")
        draw.text((col * tile + 8, y + 60), label[:12], fill=(204, 255, 255))

    draw.text((12, rows * tile + 4), "generated cyber vision samples", fill=(255, 224, 64))
    canvas.save(path)

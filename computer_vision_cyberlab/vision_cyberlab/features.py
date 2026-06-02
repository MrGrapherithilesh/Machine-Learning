from __future__ import annotations

from dataclasses import dataclass

import numpy as np


FILTER_BANK = {
    "edge_x": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float),
    "edge_y": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float),
    "laplace": np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=float),
    "soft_blur": np.ones((3, 3), dtype=float) / 9.0,
    "diagonal": np.array([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]], dtype=float),
}


@dataclass(frozen=True)
class FeatureScaler:
    mean: np.ndarray
    std: np.ndarray

    @classmethod
    def fit(cls, values: np.ndarray) -> "FeatureScaler":
        mean = values.mean(axis=0)
        std = values.std(axis=0)
        std[std < 1e-8] = 1.0
        return cls(mean=mean, std=std)

    def transform(self, values: np.ndarray) -> np.ndarray:
        return (values - self.mean) / self.std


def to_grayscale(images: np.ndarray) -> np.ndarray:
    if images.ndim != 4 or images.shape[-1] != 3:
        raise ValueError("images should have shape (n, height, width, 3)")
    weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)
    return images @ weights


def convolve_same(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    if image.ndim != 2:
        raise ValueError("image should be 2D")
    padded = np.pad(image, 1, mode="reflect")
    output = np.zeros_like(image, dtype=float)
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            patch = padded[row : row + 3, col : col + 3]
            output[row, col] = float(np.sum(patch * kernel))
    return output


def average_pool(feature_map: np.ndarray, block: int = 5) -> np.ndarray:
    if block < 2:
        raise ValueError("pool block should be at least 2")
    height, width = feature_map.shape
    pooled = []
    for row in range(0, height, block):
        for col in range(0, width, block):
            patch = feature_map[row : row + block, col : col + block]
            if patch.size:
                pooled.append(float(patch.mean()))
    return np.asarray(pooled, dtype=float)


def extract_filter_bank_features(images: np.ndarray, pool_block: int = 5) -> np.ndarray:
    gray_images = to_grayscale(images)
    rows: list[np.ndarray] = []

    for image_index, gray in enumerate(gray_images):
        channels = []
        for kernel in FILTER_BANK.values():
            response = convolve_same(gray, kernel)
            response = np.maximum(np.abs(response), 0)
            channels.append(average_pool(response, block=pool_block))

        color_mean = images[image_index].mean(axis=(0, 1))
        color_std = images[image_index].std(axis=(0, 1))
        rows.append(np.concatenate([*channels, color_mean, color_std]))

    return np.asarray(rows, dtype=float)

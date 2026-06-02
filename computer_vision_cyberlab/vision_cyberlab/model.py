from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


def _one_hot(labels: np.ndarray, class_count: int) -> np.ndarray:
    encoded = np.zeros((len(labels), class_count), dtype=float)
    encoded[np.arange(len(labels)), labels.astype(int)] = 1.0
    return encoded


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=1, keepdims=True)


@dataclass
class TinyVisionNet:
    input_dim: int
    hidden_units: int = 64
    class_count: int = 3
    seed: int = 27
    learning_rate: float = 0.06
    l2: float = 1e-4
    weights_1: np.ndarray = field(init=False)
    bias_1: np.ndarray = field(init=False)
    weights_2: np.ndarray = field(init=False)
    bias_2: np.ndarray = field(init=False)
    history: list[dict[str, float]] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        rng = np.random.default_rng(self.seed)
        self.weights_1 = rng.normal(0, np.sqrt(2 / self.input_dim), (self.input_dim, self.hidden_units))
        self.bias_1 = np.zeros(self.hidden_units)
        self.weights_2 = rng.normal(0, np.sqrt(2 / self.hidden_units), (self.hidden_units, self.class_count))
        self.bias_2 = np.zeros(self.class_count)

    def _forward(self, features: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        hidden_raw = features @ self.weights_1 + self.bias_1
        hidden = np.maximum(hidden_raw, 0)
        logits = hidden @ self.weights_2 + self.bias_2
        probabilities = _softmax(logits)
        return hidden_raw, hidden, probabilities

    def fit(self, features: np.ndarray, labels: np.ndarray, epochs: int = 90) -> "TinyVisionNet":
        y = _one_hot(labels, self.class_count)
        n = len(features)
        self.history = []

        for epoch in range(1, epochs + 1):
            hidden_raw, hidden, probabilities = self._forward(features)
            loss = -np.mean(np.sum(y * np.log(probabilities + 1e-9), axis=1))
            loss += self.l2 * (np.sum(self.weights_1**2) + np.sum(self.weights_2**2))

            grad_logits = (probabilities - y) / n
            grad_w2 = hidden.T @ grad_logits + 2 * self.l2 * self.weights_2
            grad_b2 = grad_logits.sum(axis=0)
            grad_hidden = grad_logits @ self.weights_2.T
            grad_hidden[hidden_raw <= 0] = 0
            grad_w1 = features.T @ grad_hidden + 2 * self.l2 * self.weights_1
            grad_b1 = grad_hidden.sum(axis=0)

            self.weights_2 -= self.learning_rate * grad_w2
            self.bias_2 -= self.learning_rate * grad_b2
            self.weights_1 -= self.learning_rate * grad_w1
            self.bias_1 -= self.learning_rate * grad_b1

            if epoch == 1 or epoch % 5 == 0 or epoch == epochs:
                accuracy = float(np.mean(self.predict(features) == labels))
                self.history.append(
                    {
                        "epoch": float(epoch),
                        "loss": round(float(loss), 6),
                        "accuracy": round(accuracy, 6),
                    }
                )
        return self

    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        return self._forward(features)[2]

    def predict(self, features: np.ndarray) -> np.ndarray:
        return np.argmax(self.predict_proba(features), axis=1)


def build_keras_cnn(input_shape: tuple[int, int, int] = (40, 40, 3), class_count: int = 3):
    """Optional real CNN model for users who install TensorFlow."""

    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
    from tensorflow.keras.optimizers import Adam

    model = Sequential(
        [
            Conv2D(16, (3, 3), activation="relu", input_shape=input_shape),
            MaxPooling2D((2, 2)),
            Conv2D(32, (3, 3), activation="relu"),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(64, activation="relu"),
            Dropout(0.25),
            Dense(class_count, activation="softmax"),
        ]
    )
    model.compile(optimizer=Adam(learning_rate=0.001), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model

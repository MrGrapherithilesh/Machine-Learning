from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


def _sigmoid(value: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-np.clip(value, -40, 40)))


@dataclass
class _RidgeHead:
    ridge: float = 1e-3
    output_weights: np.ndarray | None = None

    def _fit_head(self, hidden: np.ndarray, y: np.ndarray) -> None:
        design = np.c_[hidden, np.ones(len(hidden))]
        penalty = self.ridge * np.eye(design.shape[1])
        penalty[-1, -1] = 0

        left = design.T @ design + penalty
        right = design.T @ y.reshape(-1)
        try:
            self.output_weights = np.linalg.solve(left, right)
        except np.linalg.LinAlgError:
            self.output_weights = np.linalg.pinv(left) @ right

    def _predict_head(self, hidden: np.ndarray) -> np.ndarray:
        if self.output_weights is None:
            raise RuntimeError("model must be fitted before prediction")
        design = np.c_[hidden, np.ones(len(hidden))]
        return design @ self.output_weights


@dataclass
class NumpyRNNRegressor(_RidgeHead):
    hidden_units: int = 18
    seed: int = 27
    wx: np.ndarray | None = field(default=None, init=False)
    wh: np.ndarray | None = field(default=None, init=False)
    bias: np.ndarray | None = field(default=None, init=False)

    def _ensure_weights(self, input_dim: int) -> None:
        if self.wx is not None:
            return
        rng = np.random.default_rng(self.seed)
        self.wx = rng.normal(0, 0.32, (input_dim, self.hidden_units))
        self.wh = rng.normal(0, 0.18, (self.hidden_units, self.hidden_units))
        self.bias = rng.normal(0, 0.02, self.hidden_units)

    def _hidden_state(self, x: np.ndarray) -> np.ndarray:
        self._ensure_weights(x.shape[2])
        assert self.wx is not None and self.wh is not None and self.bias is not None

        states = []
        for sequence in x:
            h = np.zeros(self.hidden_units)
            for step in sequence:
                h = np.tanh(step @ self.wx + h @ self.wh + self.bias)
            states.append(h)
        return np.asarray(states)

    def fit(self, x: np.ndarray, y: np.ndarray) -> "NumpyRNNRegressor":
        self._fit_head(self._hidden_state(x), y)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.clip(self._predict_head(self._hidden_state(x)), 0, 1.2)


@dataclass
class NumpyLSTMRegressor(_RidgeHead):
    hidden_units: int = 20
    seed: int = 2701
    gate_weights: dict[str, np.ndarray] = field(default_factory=dict, init=False)
    gate_biases: dict[str, np.ndarray] = field(default_factory=dict, init=False)

    def _ensure_weights(self, input_dim: int) -> None:
        if self.gate_weights:
            return

        rng = np.random.default_rng(self.seed)
        gate_input = input_dim + self.hidden_units
        for gate in ("input", "forget", "output", "candidate"):
            self.gate_weights[gate] = rng.normal(0, 0.22, (gate_input, self.hidden_units))
            self.gate_biases[gate] = np.zeros(self.hidden_units)
        self.gate_biases["forget"] = np.full(self.hidden_units, 0.65)

    def _hidden_state(self, x: np.ndarray) -> np.ndarray:
        self._ensure_weights(x.shape[2])
        states = []

        for sequence in x:
            h = np.zeros(self.hidden_units)
            cell = np.zeros(self.hidden_units)
            for step in sequence:
                combined = np.r_[step, h]
                input_gate = _sigmoid(combined @ self.gate_weights["input"] + self.gate_biases["input"])
                forget_gate = _sigmoid(combined @ self.gate_weights["forget"] + self.gate_biases["forget"])
                output_gate = _sigmoid(combined @ self.gate_weights["output"] + self.gate_biases["output"])
                candidate = np.tanh(
                    combined @ self.gate_weights["candidate"] + self.gate_biases["candidate"]
                )
                cell = forget_gate * cell + input_gate * candidate
                h = output_gate * np.tanh(cell)
            states.append(h)

        return np.asarray(states)

    def fit(self, x: np.ndarray, y: np.ndarray) -> "NumpyLSTMRegressor":
        self._fit_head(self._hidden_state(x), y)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.clip(self._predict_head(self._hidden_state(x)), 0, 1.2)


def build_keras_rnn(input_shape: tuple[int, int]):
    """Create a Keras RNN model when TensorFlow is installed."""

    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense, Dropout, SimpleRNN
    from tensorflow.keras.optimizers import Adam

    model = Sequential(
        [
            SimpleRNN(48, return_sequences=True, input_shape=input_shape),
            Dropout(0.18),
            SimpleRNN(24),
            Dense(16, activation="relu"),
            Dense(1),
        ]
    )
    model.compile(optimizer=Adam(learning_rate=0.001), loss="mse", metrics=["mae"])
    return model


def build_keras_lstm(input_shape: tuple[int, int]):
    """Create a Keras LSTM model when TensorFlow is installed."""

    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Dense, Dropout, LSTM
    from tensorflow.keras.optimizers import Adam

    model = Sequential(
        [
            LSTM(64, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(32),
            Dense(16, activation="relu"),
            Dense(1),
        ]
    )
    model.compile(optimizer=Adam(learning_rate=0.001), loss="mse", metrics=["mae"])
    return model

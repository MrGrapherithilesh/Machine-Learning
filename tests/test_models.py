import unittest

import numpy as np

from stock_lens.models import NumpyLSTMRegressor, NumpyRNNRegressor


class ModelTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(7)
        self.x = rng.random((42, 10, 4))
        self.y = 0.55 * self.x[:, -1, 0] + 0.25 * self.x[:, -1, 1] + 0.1

    def test_rnn_predicts_finite_values(self):
        model = NumpyRNNRegressor(hidden_units=8, seed=5).fit(self.x, self.y)
        predicted = model.predict(self.x[:6])
        self.assertEqual(predicted.shape, (6,))
        self.assertTrue(np.all(np.isfinite(predicted)))

    def test_lstm_predicts_finite_values(self):
        model = NumpyLSTMRegressor(hidden_units=8, seed=5).fit(self.x, self.y)
        predicted = model.predict(self.x[:6])
        self.assertEqual(predicted.shape, (6,))
        self.assertTrue(np.all(np.isfinite(predicted)))

    def test_model_outputs_are_not_identical(self):
        rnn = NumpyRNNRegressor(hidden_units=8, seed=5).fit(self.x, self.y)
        lstm = NumpyLSTMRegressor(hidden_units=8, seed=5).fit(self.x, self.y)
        self.assertFalse(np.allclose(rnn.predict(self.x[:8]), lstm.predict(self.x[:8])))


if __name__ == "__main__":
    unittest.main()

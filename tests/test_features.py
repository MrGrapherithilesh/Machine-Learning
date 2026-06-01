import unittest

import numpy as np

from stock_lens.data import make_demo_aapl_like_data
from stock_lens.features import build_feature_frame, make_sequences, rsi


class FeatureTests(unittest.TestCase):
    def test_rsi_stays_inside_normal_bounds(self):
        prices = make_demo_aapl_like_data(days=80).frame["Close"]
        values = rsi(prices)
        self.assertTrue(np.all(values >= 0))
        self.assertTrue(np.all(values <= 100))

    def test_sequences_keep_expected_shape(self):
        price_data = make_demo_aapl_like_data(days=90)
        frame = build_feature_frame(price_data.frame)
        dataset = make_sequences(frame, window=12, horizon=1)

        self.assertEqual(dataset.x.shape[1], 12)
        self.assertEqual(dataset.x.shape[2], len(dataset.feature_columns))
        self.assertEqual(dataset.x.shape[0], dataset.y.shape[0])

    def test_inverse_close_scaling(self):
        price_data = make_demo_aapl_like_data(days=90)
        frame = build_feature_frame(price_data.frame)
        dataset = make_sequences(frame, window=12)
        restored = dataset.scaler.inverse_column(dataset.y[:3], "Close")

        self.assertEqual(restored.shape, (3,))
        self.assertTrue(np.all(restored > 0))


if __name__ == "__main__":
    unittest.main()

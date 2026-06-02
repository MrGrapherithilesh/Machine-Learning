import unittest

import numpy as np

from vision_cyberlab.dataset import make_dataset
from vision_cyberlab.features import FeatureScaler, convolve_same, extract_filter_bank_features, to_grayscale


class FeatureTests(unittest.TestCase):
    def test_grayscale_conversion(self):
        dataset = make_dataset(samples_per_class=10, image_size=28, seed=4)
        gray = to_grayscale(dataset.images)

        self.assertEqual(gray.shape, (30, 28, 28))

    def test_convolution_keeps_image_size(self):
        image = np.eye(8)
        kernel = np.ones((3, 3)) / 9
        response = convolve_same(image, kernel)

        self.assertEqual(response.shape, image.shape)
        self.assertTrue(np.all(np.isfinite(response)))

    def test_feature_scaler_normalises_values(self):
        dataset = make_dataset(samples_per_class=12, image_size=32, seed=5)
        features = extract_filter_bank_features(dataset.images)
        scaler = FeatureScaler.fit(features)
        scaled = scaler.transform(features)

        self.assertEqual(features.shape[0], 36)
        self.assertLess(abs(float(scaled.mean())), 1e-6)


if __name__ == "__main__":
    unittest.main()

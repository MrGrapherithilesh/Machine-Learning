import unittest

import numpy as np

from vision_cyberlab.dataset import make_dataset
from vision_cyberlab.features import FeatureScaler, extract_filter_bank_features
from vision_cyberlab.model import TinyVisionNet


class ModelTests(unittest.TestCase):
    def test_tiny_vision_net_learns_generated_patterns(self):
        dataset = make_dataset(samples_per_class=35, image_size=32, seed=8)
        features_raw = extract_filter_bank_features(dataset.images)
        features = FeatureScaler.fit(features_raw).transform(features_raw)

        model = TinyVisionNet(input_dim=features.shape[1], hidden_units=36, seed=8, learning_rate=0.05)
        model.fit(features, dataset.labels, epochs=45)
        predicted = model.predict(features)
        accuracy = np.mean(predicted == dataset.labels)

        self.assertGreater(accuracy, 0.82)
        self.assertEqual(model.predict_proba(features[:4]).shape, (4, 3))


if __name__ == "__main__":
    unittest.main()

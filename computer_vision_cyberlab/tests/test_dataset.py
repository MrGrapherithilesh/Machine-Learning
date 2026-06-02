import unittest

from vision_cyberlab.dataset import LABELS, make_dataset


class DatasetTests(unittest.TestCase):
    def test_dataset_shape_and_balance(self):
        dataset = make_dataset(samples_per_class=18, image_size=32, seed=3)

        self.assertEqual(dataset.images.shape, (54, 32, 32, 3))
        self.assertEqual(dataset.labels.shape, (54,))
        self.assertEqual(set(dataset.class_counts().keys()), set(LABELS))
        self.assertTrue(all(count == 18 for count in dataset.class_counts().values()))


if __name__ == "__main__":
    unittest.main()

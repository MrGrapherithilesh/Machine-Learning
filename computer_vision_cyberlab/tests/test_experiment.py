import tempfile
import unittest
from pathlib import Path

from vision_cyberlab.experiment import run_experiment


class ExperimentTests(unittest.TestCase):
    def test_experiment_writes_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_experiment(output_dir=tmp, samples_per_class=30, image_size=32, epochs=45)
            output = Path(tmp)

            self.assertTrue((output / "metrics.json").exists())
            self.assertTrue((output / "predictions.csv").exists())
            self.assertTrue((output / "confusion_matrix.png").exists())
            self.assertGreaterEqual(result.metrics["test_report"]["accuracy"], 0.75)


if __name__ == "__main__":
    unittest.main()

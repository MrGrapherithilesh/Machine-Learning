import tempfile
import unittest
from pathlib import Path

from stock_lens.experiment import run_experiment


class ExperimentTests(unittest.TestCase):
    def test_experiment_writes_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_experiment(output_dir=tmp, days=145, window=12)
            output = Path(tmp)

            self.assertTrue((output / "metrics.json").exists())
            self.assertTrue((output / "predictions.csv").exists())
            self.assertTrue((output / "prediction_plot.png").exists())
            self.assertIn("lstm", result.metrics["models"])
            self.assertGreater(len(result.predictions), 5)


if __name__ == "__main__":
    unittest.main()

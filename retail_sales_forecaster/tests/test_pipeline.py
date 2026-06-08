import importlib.util
from pathlib import Path


def load_main_module():
    project_dir = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location('project_main', project_dir / 'main.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pipeline_creates_metrics_and_preview():
    module = load_main_module()
    metrics = module.run_pipeline()
    assert isinstance(metrics, dict)
    assert (module.OUTPUT_DIR / 'metrics.json').exists()
    assert (module.SCREENSHOT_DIR / 'dashboard.png').exists()
    assert (module.SCREENSHOT_DIR / 'ui_preview.html').exists()

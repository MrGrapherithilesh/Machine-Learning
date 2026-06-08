import importlib.util
from pathlib import Path


def load_project():
    project_dir = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location('project_main', project_dir / 'main.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pipeline_outputs_files():
    module = load_project()
    metrics = module.run_pipeline()
    project_dir = Path(__file__).resolve().parents[1]
    assert isinstance(metrics, dict)
    assert (project_dir / 'outputs' / 'metrics.json').exists()
    assert (project_dir / 'screenshots' / 'dashboard.png').exists()
    assert (project_dir / 'screenshots' / 'ui_preview.html').exists()

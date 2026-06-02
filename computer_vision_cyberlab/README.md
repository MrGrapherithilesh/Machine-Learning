# Deep Learning for Computer Vision using Python and MATLAB

This project demonstrates a computer vision deep learning workflow with a cyberpunk themed dashboard, Python model code, MATLAB reference scripts, tests, and captured outputs.

The project trains a tiny neural network to classify synthetic vision samples. The images are generated with noisy neon patterns, then Python extracts convolution-style filter-bank features and trains a small ReLU + Softmax network. MATLAB scripts show how the same idea can be represented with image datastores and CNN layers.

## Idea

Computer vision models learn from image patterns like edges, shapes, colors and texture. CNNs are powerful because convolution layers scan the image with filters instead of treating every pixel like a separate random number. This project keeps that concept simple:

- generate small image samples for three classes
- pass each image through edge and texture filters
- pool the responses into compact features
- train a tiny deep learning classifier
- show accuracy, confusion matrix, training curve and sample predictions in a cyberpunk UI

## Classes

- `neon_square`
- `pulse_ring`
- `diagonal_strike`

## Files

- `vision_cyberlab/` - Python source code
- `matlab/` - MATLAB reference implementation
- `tests/` - unit tests
- `outputs/` - captured run output and screenshots

## Screenshots

![Dashboard](outputs/ui-dashboard.png)

![Test output](outputs/test-output.png)

## Run

```bash
python -m vision_cyberlab.cli run --output outputs
python -m vision_cyberlab.cli serve --port 8790
```

Open:

```text
http://127.0.0.1:8790
```

Tests:

```bash
python -m unittest discover -v
```

## MATLAB part

Open `matlab/cyberVisionDemo.m` in MATLAB. It shows the same pipeline in MATLAB style:

- image datastore
- CNN layers
- training options
- prediction
- confusion chart

MATLAB is not required for the native run. The Python project runs fully on its own, and the MATLAB files are included as the reference workflow.

## Final note

This is a learning project, not a production vision system. It covers dataset generation, feature extraction, neural network training, testing, output capture, and dashboard presentation.

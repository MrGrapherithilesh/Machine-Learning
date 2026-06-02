# Machine-Learning

ML projects made by me. I am keeping this repo like a proper AIML portfolio dump, not just one random readme and empty folders.

## Projects

### 1. Stock Price Prediction using LSTM and RNN

Apple stock prediction using time-series windows, RSI, EMA, RNN and LSTM style models.

- Code: `stock_lens/`
- Output screenshots: `outputs/`
- Run:

```bash
python -m stock_lens.cli run --symbol AAPL --demo-data --output outputs
python -m stock_lens.cli serve --port 8765
```

![Stock dashboard](outputs/ui-dashboard.png)

### 2. Deep Learning for Computer Vision using Python and MATLAB

Cyberpunk themed computer vision project using Python for the working model and MATLAB files for the equivalent deep learning workflow.

- Code: `computer_vision_cyberlab/`
- Output screenshots: `computer_vision_cyberlab/outputs/`
- Run:

```bash
cd computer_vision_cyberlab
python -m vision_cyberlab.cli run --output outputs
python -m vision_cyberlab.cli serve --port 8790
```

![Computer vision dashboard](computer_vision_cyberlab/outputs/ui-dashboard.png)

## My note

I am 21 and studying AIML, so these projects are written in a student style but still made to run properly. Theory is there, code is tested, output is captured, and the UI is not boring.

const state = {
  metrics: null,
  predictions: [],
  view: "scan",
  mode: "python",
  threshold: 70,
};

const images = {
  scan: "/outputs/training_curve.png",
  matrix: "/outputs/confusion_matrix.png",
  samples: "/outputs/prediction_mosaic.png",
};

const copy = {
  python: `TinyVisionNet

filters:
  edge_x
  edge_y
  laplace
  soft_blur
  diagonal

layers:
  input features
  dense relu 72
  softmax head

optimizer:
  gradient descent
  cross entropy`,
  matlab: `MATLAB mirror

imageInputLayer
conv2d 16 filters
batchNorm + relu
maxPool
conv2d 32 filters
fullyConnected 64
dropout
softmax
classificationLayer`,
};

const viewTitles = {
  scan: ["training curve", "Python native run"],
  matrix: ["confusion matrix", "Class prediction heat"],
  samples: ["sample predictions", "Neon dataset inspection"],
};

const byId = (id) => document.getElementById(id);

async function loadData() {
  const [metricsResponse, predictionsResponse] = await Promise.all([
    fetch("/outputs/metrics.json"),
    fetch("/outputs/predictions.csv"),
  ]);

  if (!metricsResponse.ok || !predictionsResponse.ok) {
    throw new Error("output files missing");
  }

  state.metrics = await metricsResponse.json();
  state.predictions = parseCsv(await predictionsResponse.text());
  render();
}

function parseCsv(text) {
  const [headerLine, ...lines] = text.trim().split(/\r?\n/);
  const headers = headerLine.split(",");
  return lines.map((line) => {
    const values = line.split(",");
    const row = {};
    headers.forEach((header, index) => {
      const value = values[index];
      if (["sample_id", "actual_id", "predicted_id"].includes(header)) {
        row[header] = Number(value);
      } else if (header === "confidence") {
        row[header] = Number(value);
      } else if (header === "correct") {
        row[header] = value === "True";
      } else {
        row[header] = value;
      }
    });
    return row;
  });
}

function render() {
  if (!state.metrics) {
    return;
  }

  byId("accuracy").textContent = `${(state.metrics.test_report.accuracy * 100).toFixed(1)}%`;
  byId("samples").textContent = state.metrics.samples;
  byId("features").textContent = state.metrics.feature_count;
  byId("loss").textContent = state.metrics.model.final_train_loss.toFixed(3);
  byId("stage-label").textContent = viewTitles[state.view][0];
  byId("stage-title").textContent = viewTitles[state.view][1];
  byId("stage-image").src = images[state.view];
  byId("stack-copy").textContent = copy[state.mode];
  byId("mode-label").textContent = state.mode === "python" ? "PY" : "ML";
  byId("confidence-value").textContent = state.threshold;
  renderTable();
}

function renderTable() {
  const rows = state.predictions
    .filter((row) => row.confidence * 100 >= state.threshold)
    .slice(0, 10);

  byId("filtered-count").textContent = `${rows.length} shown`;
  byId("prediction-table").innerHTML = rows.map((row) => `
    <tr>
      <td>#${String(row.sample_id).padStart(3, "0")}</td>
      <td>${row.actual.replaceAll("_", " ")}</td>
      <td class="${row.correct ? "good" : "bad"}">${row.predicted.replaceAll("_", " ")}</td>
      <td>${(row.confidence * 100).toFixed(1)}%</td>
    </tr>
  `).join("");
}

function bindControls() {
  document.querySelectorAll(".rail-button").forEach((button) => {
    button.addEventListener("click", () => {
      state.view = button.dataset.view;
      document.querySelectorAll(".rail-button").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      render();
    });
  });

  document.querySelectorAll(".mode").forEach((button) => {
    button.addEventListener("click", () => {
      state.mode = button.dataset.mode;
      document.querySelectorAll(".mode").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      render();
    });
  });

  byId("confidence-range").addEventListener("input", (event) => {
    state.threshold = Number(event.target.value);
    render();
  });

  byId("heat-toggle").addEventListener("change", (event) => {
    document.querySelector(".visual-stage").classList.toggle("no-heat", !event.target.checked);
  });
}

bindControls();
loadData().catch((error) => {
  byId("stage-title").textContent = "run the experiment first";
  byId("stage-label").textContent = error.message;
});

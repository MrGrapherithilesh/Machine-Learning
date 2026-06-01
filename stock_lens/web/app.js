const state = {
  model: "lstm",
  predictions: [],
  metrics: null,
  showActual: true,
  days: 110,
  hoverIndex: null,
};

const money = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2,
});

const byId = (id) => document.getElementById(id);

async function loadData() {
  const [metricsResponse, predictionResponse] = await Promise.all([
    fetch("../outputs/metrics.json"),
    fetch("../outputs/predictions.csv"),
  ]);

  if (!metricsResponse.ok || !predictionResponse.ok) {
    throw new Error("run output is missing");
  }

  state.metrics = await metricsResponse.json();
  state.predictions = parseCsv(await predictionResponse.text());
  byId("source").textContent = state.metrics.source;
  byId("window").textContent = `${state.metrics.window} days`;
  updateScreen();
}

function parseCsv(text) {
  const [headerLine, ...lines] = text.trim().split(/\r?\n/);
  const headers = headerLine.split(",");
  return lines.map((line) => {
    const cells = line.split(",");
    const row = {};
    headers.forEach((header, index) => {
      const value = cells[index];
      row[header] = header === "date" ? value : Number(value);
    });
    return row;
  });
}

function updateScreen() {
  const modelMetrics = state.metrics.models[state.model];
  byId("rmse").textContent = modelMetrics.rmse.toFixed(2);
  byId("mae").textContent = modelMetrics.mae.toFixed(2);
  byId("mape").textContent = `${modelMetrics.mape.toFixed(2)}%`;
  byId("direction").textContent = `${modelMetrics.direction_accuracy.toFixed(1)}%`;

  const latest = state.predictions[state.predictions.length - 1];
  const predictionKey = `${state.model}_prediction`;
  const gap = latest[predictionKey] - latest.actual_close;
  byId("latest").textContent = `${state.model.toUpperCase()} call for ${latest.date}`;
  byId("last-close").textContent = money.format(latest.actual_close);
  byId("last-prediction").textContent = money.format(latest[predictionKey]);
  byId("gap").textContent = `${gap >= 0 ? "+" : ""}${money.format(gap)}`;
  byId("days-value").textContent = state.days;

  renderTable();
  drawChart();
}

function renderTable() {
  const rows = state.predictions.slice(-7).reverse();
  byId("prediction-table").innerHTML = rows.map((row) => `
    <tr>
      <td>${row.date}</td>
      <td>${money.format(row.actual_close)}</td>
      <td>${money.format(row.rnn_prediction)}</td>
      <td>${money.format(row.lstm_prediction)}</td>
    </tr>
  `).join("");
}

function drawChart() {
  if (!state.predictions.length) {
    return;
  }

  const canvas = byId("price-chart");
  const ctx = canvas.getContext("2d");
  const ratio = window.devicePixelRatio || 1;
  const bounds = canvas.getBoundingClientRect();
  canvas.width = Math.floor(bounds.width * ratio);
  canvas.height = Math.floor(bounds.height * ratio);
  ctx.scale(ratio, ratio);

  const width = bounds.width;
  const height = bounds.height;
  const pad = { left: 58, right: 22, top: 24, bottom: 42 };
  const plotWidth = width - pad.left - pad.right;
  const plotHeight = height - pad.top - pad.bottom;
  const rows = state.predictions.slice(-state.days);
  const predictionKey = `${state.model}_prediction`;

  const values = rows.flatMap((row) => state.showActual
    ? [row.actual_close, row[predictionKey]]
    : [row[predictionKey]]);
  const minValue = Math.min(...values) * 0.995;
  const maxValue = Math.max(...values) * 1.005;

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#090907";
  ctx.fillRect(0, 0, width, height);
  ctx.strokeStyle = "#2f2a1d";
  ctx.lineWidth = 1;

  for (let i = 0; i <= 5; i += 1) {
    const y = pad.top + (plotHeight * i) / 5;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(width - pad.right, y);
    ctx.stroke();
    const label = maxValue - ((maxValue - minValue) * i) / 5;
    ctx.fillStyle = "#aaa38c";
    ctx.fillText(`$${label.toFixed(0)}`, 8, y + 4);
  }

  const xFor = (index) => pad.left + (plotWidth * index) / Math.max(rows.length - 1, 1);
  const yFor = (value) => pad.top + plotHeight - ((value - minValue) / (maxValue - minValue)) * plotHeight;

  if (state.showActual) {
    drawLine(ctx, rows, "actual_close", xFor, yFor, "#fff1a8", 3);
  }
  drawLine(ctx, rows, predictionKey, xFor, yFor, "#ffd43b", 3);

  ctx.fillStyle = "#aaa38c";
  ctx.fillText(rows[0].date, pad.left, height - 14);
  ctx.fillText(rows[rows.length - 1].date, width - pad.right - 78, height - 14);

  if (state.hoverIndex !== null && rows[state.hoverIndex]) {
    const row = rows[state.hoverIndex];
    const x = xFor(state.hoverIndex);
    ctx.strokeStyle = "#f7f2df";
    ctx.beginPath();
    ctx.moveTo(x, pad.top);
    ctx.lineTo(x, height - pad.bottom);
    ctx.stroke();
    showTooltip(canvas, row, x, yFor(row[predictionKey]));
  } else {
    byId("tooltip").hidden = true;
  }
}

function drawLine(ctx, rows, key, xFor, yFor, color, lineWidth) {
  ctx.strokeStyle = color;
  ctx.lineWidth = lineWidth;
  ctx.beginPath();
  rows.forEach((row, index) => {
    const x = xFor(index);
    const y = yFor(row[key]);
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });
  ctx.stroke();
}

function showTooltip(canvas, row, x, y) {
  const tooltip = byId("tooltip");
  const predictionKey = `${state.model}_prediction`;
  tooltip.innerHTML = `
    <strong>${row.date}</strong><br>
    actual: ${money.format(row.actual_close)}<br>
    ${state.model.toUpperCase()}: ${money.format(row[predictionKey])}
  `;
  tooltip.hidden = false;
  tooltip.style.left = `${Math.min(x + 28, canvas.offsetLeft + canvas.clientWidth - 210)}px`;
  tooltip.style.top = `${Math.max(78, y + 70)}px`;
}

function bindControls() {
  document.querySelectorAll(".model-button").forEach((button) => {
    button.addEventListener("click", () => {
      state.model = button.dataset.model;
      document.querySelectorAll(".model-button").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      updateScreen();
    });
  });

  byId("actual-toggle").addEventListener("change", (event) => {
    state.showActual = event.target.checked;
    drawChart();
  });

  byId("days-range").addEventListener("input", (event) => {
    state.days = Number(event.target.value);
    state.hoverIndex = null;
    updateScreen();
  });

  byId("price-chart").addEventListener("mousemove", (event) => {
    const rows = state.predictions.slice(-state.days);
    const bounds = event.currentTarget.getBoundingClientRect();
    const x = event.clientX - bounds.left;
    const plotLeft = 58;
    const plotRight = bounds.width - 22;
    if (x < plotLeft || x > plotRight) {
      state.hoverIndex = null;
    } else {
      state.hoverIndex = Math.round(((x - plotLeft) / (plotRight - plotLeft)) * (rows.length - 1));
    }
    drawChart();
  });

  byId("price-chart").addEventListener("mouseleave", () => {
    state.hoverIndex = null;
    drawChart();
  });

  window.addEventListener("resize", drawChart);
}

bindControls();
loadData().catch((error) => {
  byId("latest").textContent = "run the experiment first";
  byId("source").textContent = error.message;
});

document.querySelectorAll("table").forEach((table) => {
  table.addEventListener("mouseover", (event) => {
    const row = event.target.closest("tr");
    if (row) row.style.background = "#f7fbff";
  });
  table.addEventListener("mouseout", (event) => {
    const row = event.target.closest("tr");
    if (row) row.style.background = "";
  });
});


function createGraphs(data = [0, 0], data2 = [0, 0], categoryNames = []) {
  console.log(categoryNames);
  const ctx1 = document.getElementById("graph1");
  const ctx2 = document.getElementById("graph2");

  // Colors
  const computedStyle = getComputedStyle(document.documentElement);
  const primaryColor = computedStyle.getPropertyValue("--primary");
  const foregroundColor = computedStyle.getPropertyValue("--foreground");
  const green = "hsl(142 76% 36% / 0.5)";
  const red = "hsl(0 72% 51% / 0.5)";
  const blue = "hsl(221 83% 53% / 0.5)";

  // Defaults
  Chart.defaults.borderColor = `hsl(${foregroundColor}/0.2)`;

  new Chart(ctx1, {
    type: "pie",
    data: {
      labels: ["Correct", "Incorrect", "Unanswered"],
      datasets: [
        {
          label: "Quantities",
          data,
          borderWidth: 1,
          borderColor: `hsl(${foregroundColor}/0.5)`,
          backgroundColor: [green, red, blue],
          hoverBackgroundColor: [
            green.replace("0.5", "0.7"),
            red.replace("0.5", "0.7"),
            blue.replace("0.5", "0.7"),
          ],
        },
      ],
    },
  });

  new Chart(ctx2, {
    type: "polarArea",
    data: {
      labels: categoryNames,
      datasets: [
        {
          label: "Hits",
          data: data2,
          fill: true,
          borderWidth: 1,
          borderColor: `hsl(${primaryColor})`,
          backgroundColor: `hsl(${primaryColor}/0.2)`,
          hoverBackgroundColor: `hsl(${primaryColor}/0.4)`,
          pointBackgroundColor: `hsl(${primaryColor})`,
          pointBorderColor: `hsl(${foregroundColor})`,
          pointHoverBackgroundColor: `hsl(${foregroundColor})`,
          pointHoverBorderColor: `hsl(${primaryColor})`,
        },
      ],
    },
  });
}

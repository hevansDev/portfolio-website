google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

fetch('http://hughevans.dev:5000/moisture')
  .then(response => response.json())
  .then(json => console.log(json));

function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ["Plant", "Moisture", { role: "style" } ],
    ["Bilberry Cactus", 8.94, "#b87333"],
    ["Cast-Iron Plant", 10.49, "silver"],
    ["Pothos", 19.30, "gold"]
  ]);

  var view = new google.visualization.DataView(data);
  view.setColumns([0, 1,
                   { calc: "stringify",
                     sourceColumn: 1,
                     type: "string",
                     role: "annotation" },
                   2]);

  var options = {
    title: "Grow Dashboard",
    width: 600,
    height: 400,
    bar: {groupWidth: "95%"},
    legend: { position: "none" },
  };
  var chart = new google.visualization.BarChart(document.getElementById("barchart_values"));
  chart.draw(view, options);
}

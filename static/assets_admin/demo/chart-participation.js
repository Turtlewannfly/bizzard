// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
fetch('/admin/participation-chart')
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById("ParticipationChart");
        let maxValue = parseInt(Math.max(...data.values)) + 1;
        var myLineChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [{
              backgroundColor: "rgba(235, 199, 0, 1)",
              borderColor: "rgba(235, 199, 0, 1)",
              data: data.values,
            }],
          },
          options: {
            scales: {
              xAxes: [{
                gridLines: {
                  display: false
                },
              }],
              
              yAxes: [{
                ticks: {
                  min: 0,
                  max: maxValue,
                },
                gridLines: {
                  display: true
                }
              }],
              
            },
            legend: {
              display: false
            },
            "animation": {
              "duration": 1,
              "onComplete": function() {
                var chartInstance = this.chart
                ctx = chartInstance.ctx;
                ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
                ctx.fillStyle = this.chart.config.options.defaultFontColor;
                ctx.textAlign = 'left';
                ctx.textBaseline = 'bottom';

                this.data.datasets.forEach(function(dataset, i) {
                  var meta = chartInstance.controller.getDatasetMeta(i);
                  meta.data.forEach(function(bar, index) {
                        var data = dataset.data[index];
                        ctx.fillText(data, bar._model.x -2, bar._model.y - 5);
                  });
                });
              }
            },
          }
        });
    });

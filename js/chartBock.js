Chart.defaults.global.defaultFontFamily = 'Roboto';
Chart.defaults.global.defaultFontColor = '#333';
function returnAVG(row) {
    sum = 0;
    for (let i = 1; i < row.length; i++) {
        sum += row[i];
    }
    return sum / (row.length-1);
}
function makeChart(today, City) {
  
    var ctx = document.getElementById('chart' + City).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Object.keys(today),
            datasets: [
            {
                label: 'Today',
                //data = today[key]['TODAY'][0]
                data: Object.values(today).map(function(row) {
                    return row['TODAY'][2];
                }),
                percent: Object.values(today).map(function(row) {
                  return row['TODAY'][0];
                }),
                // color blue
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
            },
            {
                label: 'Average',
                //data = today[key]['AVG'][0]
                data: Object.values(today).map(function(row) {
                    return row['AVG'][2];
                }),
                // save the average value
                percent: Object.values(today).map(function(row) {
                    return row['AVG'][0];
                }),
                // color red
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
            }
            ]
        },
        options: {
          tooltips: {
            mode: 'index',
            intersect: false,
            //show average on hover
            callbacks: {
              label: function(tooltipItem, data) {
                var label = data.datasets[tooltipItem.datasetIndex].label || '';
                if (label) {
                  label += ': ';
                }
                label += data.datasets[tooltipItem.datasetIndex].percent[tooltipItem.index] + '%';
                return label;
              }
            }
         },
         hover: {
            mode: 'index',
            intersect: false
         },
         legend: {
          labels: {
              fontColor: "white",
              fontSize: 18
          }
          },
          scales: {
            yAxes: [{
                ticks: {
                    fontColor: "white",
                    beginAtZero: true
                }
            }],
            xAxes: [{
                ticks: {
                    fontColor: "white",
                    stepSize: 60,
                }
            }]
          },

        
        
          annotation: {
            annotations: {
              line1: {
                type: 'line',
                yMin: 60,
                yMax: 60,
                borderColor: 'rgb(255, 99, 132)',
                borderWidth: 2,
              }
            }
          }

        }
    });
      
}
Cities = ['Nürnberg', 'Zirndorf', 'Erlangen', 'Konstanz', 'Passau']
Cities.forEach(City => {
  d3.json("today/" + City + "Belegung.json").then(function(data) {
    makeChart(data, City);
  });
});

        
    
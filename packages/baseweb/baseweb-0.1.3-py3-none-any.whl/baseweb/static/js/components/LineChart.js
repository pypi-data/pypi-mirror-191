Vue.component('line-chart', {
  extends:  VueChartJs.Line,
  mixins: [ VueChartJs.mixins.reactiveProp ],
  props:  [ "options" ],
  mounted: function() {
    this.renderChart(
      this.chartData,
      {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        animation: {
          duration: 0
        },
        scales: {
          yAxes: [{
            display: true,
            ticks: {
              suggestedMin: 0,
              beginAtZero: true   // minimum value will be 0.
            }
          }]
        }
      }
    );
  }
});

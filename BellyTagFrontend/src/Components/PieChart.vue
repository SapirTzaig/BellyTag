<template>
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from "chart.js";
  
  Chart.register(...registerables);
  
  export default {
    props: {
      value: Number,
      min: Number,
      max: Number
    },
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        const ctx = this.$refs.chartCanvas.getContext("2d");
  
        new Chart(ctx, {
          type: "doughnut",
          data: {
            labels: ["Your Value", "Normal Range"],
            datasets: [
              {
                data: [this.value, this.max - this.min],
                backgroundColor: ["#FF6384", "#36A2EB"],
                hoverBackgroundColor: ["#FF6384", "#36A2EB"]
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .chart-container {
    width: 100px;
    height: 100px;
    margin: 10px auto;
  }
  </style>
  
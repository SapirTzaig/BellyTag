<template>
    <div class="nt-details-container">
      <h2>Nuchal Translucency Screening - Detailed Report</h2>
  
      <!-- גרף NT לאורך ההריון -->
      <div class="chart-container">
        <LineChart :chart-data="chartData" :chart-options="chartOptions" />
      </div>
  
      <!-- טבלה עם נתוני בדיקות -->
      <table class="nt-table">
        <thead>
          <tr>
            <th>Week</th>
            <th>NT (mm)</th>
            <th>CRL (mm)</th>
            <th>BPD (mm)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="test in ntTests" :key="test.week">
            <td>{{ test.week }}</td>
            <td>{{ test.nt }}</td>
            <td>{{ test.crl }}</td>
            <td>{{ test.bpd }}</td>
          </tr>
        </tbody>
      </table>
  
      <!-- חזרה לדף הראשי -->
      <button @click="goBack">Back</button>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref } from "vue";
  import { LineChart } from "vue-chart-3";
  import { Chart, registerables } from "chart.js";
  import { useRouter } from "vue-router";
  
  Chart.register(...registerables);
  
  export default defineComponent({
    components: { LineChart },
    setup() {
      const router = useRouter();
  
      // נתוני בדיקות קודמות
      const ntTests = ref([
        { week: "Week 12", nt: 1.9, crl: 73.4, bpd: 23.5 },
        { week: "Week 16", nt: 2.2, crl: 85.1, bpd: 26.8 },
        { week: "Week 20", nt: 2.5, crl: 97.2, bpd: 30.3 },
      ]);
  
      // נתוני גרף
      const chartData = ref({
        labels: ntTests.value.map((test) => test.week),
        datasets: [
          {
            label: "NT Measurement (mm)",
            data: ntTests.value.map((test) => test.nt),
            borderColor: "blue",
            backgroundColor: "rgba(0, 0, 255, 0.2)",
            fill: true,
          },
        ],
      });
  
      // אפשרויות גרף
      const chartOptions = ref({
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "top" } },
        scales: { y: { beginAtZero: false } },
      });
  
      const goBack = () => {
        router.push("/");
      };
  
      return { ntTests, chartData, chartOptions, goBack };
    },
  });
  </script>
  
  <style scoped>
  .nt-details-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

  
.chart-container {
  height: 250px; /* הגבלת הגובה */
  max-height: 350px;
  width: 150%; /* התאמת הרוחב */
  overflow: hidden;
  margin-bottom: 40px; /* יותר רווח מהטבלה */
  display: flex;
  justify-content: center;
}


  
  .nt-table {
    width: 80%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  .nt-table th,
  .nt-table td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  
  .nt-table th {
    background-color: #f4f4f4;
  }
  
  button {
    padding: 8px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  
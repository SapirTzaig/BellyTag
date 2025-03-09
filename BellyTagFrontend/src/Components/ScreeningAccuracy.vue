<template>
    <div class="screening-accuracy-card">
      <h3>Screening Accuracy</h3>
      <p><strong>False Positive Risk:</strong> {{ falsePositiveRisk }}%</p>
      <p><strong>False Negative Risk:</strong> {{ falseNegativeRisk }}%</p>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      falsePositiveRisk: Number,
      falseNegativeRisk: Number
    }
  };
  </script>
  
  <style scoped>
  .screening-accuracy-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    min-height: 150px;
  }
  </style>
  
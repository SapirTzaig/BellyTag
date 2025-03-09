<template>
    <div class="gbs-test-card">
      <h3>Group B Streptococcus Test</h3>
      <p><strong>Result:</strong> {{ gbsResult ? "Positive ❌" : "Negative ✅" }}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      gbsResult: Boolean
    }
  };
  </script>
  
  <style scoped>
  .gbs-test-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    min-height: 150px;
  }
  </style>
  
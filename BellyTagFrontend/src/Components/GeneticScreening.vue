<template>
    <div class="genetic-screening-card">
      <h3>Genetic Screening Recommendation</h3>
      <p><strong>Genetic Counseling:</strong> {{ geneticCounseling ? "Recommended ✅" : "Not Needed ❌" }}</p>
      <p><strong>Additional Testing:</strong> {{ additionalTesting ? "Needed ✅" : "Not Needed ❌" }}</p>
      <p v-if="additionalTests.length">
        <strong>Recommended Tests:</strong> {{ additionalTests.join(", ") }}
      </p>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      geneticCounseling: Boolean,
      additionalTesting: Boolean,
      additionalTests: Array
    }
  };
  </script>
  
  <style scoped>
  .genetic-screening-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    min-height: 150px;
  }
  </style>
  
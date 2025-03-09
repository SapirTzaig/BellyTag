<template>
    <div class="follow-up-tests-card">
      <h3>Follow-up Testing</h3>
      <p><strong>Ultrasound Needed:</strong> {{ ultrasoundNeeded ? "Yes ✅" : "No ❌" }}</p>
      <p><strong>Amniocentesis Needed:</strong> {{ amniocentesisNeeded ? "Yes ✅" : "No ❌" }}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      ultrasoundNeeded: Boolean,
      amniocentesisNeeded: Boolean
    }
  };
  </script>
  
  <style scoped>
  .follow-up-tests-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    min-height: 150px;
  }
  </style>
  
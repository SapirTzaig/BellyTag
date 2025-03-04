<template>
    <div class="patient-screen">
      <h1>Patient: {{ patient.username }}</h1>
      <!-- Display patient information here -->
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        patient: {}
      };
    },
    async created() {
      const patientId = this.$route.params.id;
      const response = await fetch('http://localhost:5000/patient/' + patientId);
      const data = await response.json();
      this.patient = data;
    }
  };
  </script>
  
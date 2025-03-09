<template>
    <div class="patient-screen">
      <h1>Patient: {{ patient.username }}</h1>
  
      <div class="components-grid">
        <PregnancyWeek :lastPeriodDate="patient.LastPeriodDate" />
        <BloodTests />
        <LastPeriodDate :lastPeriodDate="patient.LastPeriodDate" @update-date="updateLastPeriodDate" />
        <NuchalTranslucencySummary :nt-value="patient.ntValue" />
      </div>
  
      <button class="logout-btn" @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  import PregnancyWeek from "@/Components/PregnancyWeek.vue";
  import BloodTests from "@/Components/BloodTests.vue";
  import LastPeriodDate from "@/Components/LastPeriodDate.vue";
  import NuchalTranslucencySummary from "@/Components/NuchalTranslucencySummary.vue";
  
  export default {
    components: {
      PregnancyWeek,
      BloodTests,
      LastPeriodDate,
      NuchalTranslucencySummary,
    },
    data() {
      return {
        patient: {},
      };
    },
    async created() {
      try {
        // ✅ Use the correct sessionStorage key for patient
        const patientBarcode = sessionStorage.getItem("patientBarcode");
  
        if (!patientBarcode) {
          alert("No patient selected.");
          this.$router.push("/dashboard");
          return;
        }
  
        const response = await fetch(`http://localhost:5000/personal?barcode=${patientBarcode}`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });
  
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
  
        const data = await response.json();
  
        this.patient = {
          username: data.Name || "Unknown",
          PregnancyWeek: data.PregnancyWeek || 0,
          LastPeriodDate: data.LastPeriodDate || "N/A",
          ntValue: data.NuchalTranslucencyValue || "N/A",
        };
      } catch (error) {
        console.error("❌ Error fetching patient details:", error);
      }
    },
    methods: {
      logout() {
        sessionStorage.removeItem("patientBarcode"); // ✅ Remove only patient data on logout
        alert("Logged out successfully!");
        this.$router.push("/");
      },
    },
  };
  </script>
  
  <style scoped>
  .patient-screen {
    text-align: center;
    padding-top: 80px;
  }
  
  .components-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    max-width: 1200px;
    margin: 20px auto;
    padding: 20px;
  }
  
  .logout-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #e74c3c;
    border: none;
    color: white;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .logout-btn:hover {
    background-color: #c0392b;
  }
  </style>
  
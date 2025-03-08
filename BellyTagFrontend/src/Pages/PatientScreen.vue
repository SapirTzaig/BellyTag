<template>
  <div class="patient-screen">
    <h1>Patient: {{ patient.username }}</h1>

    <div class="components-grid">
      <PregnancyWeek :lastPeriodDate="patient.LastPeriodDate" />
      <BloodTests />
      <LastPeriodDate :lastPeriodDate="patient.LastPeriodDate" @update-date="updateLastPeriodDate" />
      <NuchalTranslucencySummary :nt-value="patient.ntValue" />
    </div>
  </div>
</template>

<script>
import logoImage from "@/Assets/logo.png";
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
      logoImage,
      tableauURL: "https://public.tableau.com/shared/37ZW4WCT6?:display_count=n&:origin=viz_share_link",
      barcode: sessionStorage.getItem("barcode") || "", // Get the barcode from sessionStorage
    };
  },
  async created() {
    try {
      const patientId = sessionStorage.getItem('barcode');
      const response = await fetch(`http://localhost:5000/personal?barcode=${patientId}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      const data = await response.json();

      this.patient = {
        username: data.Name || "Unknown",
        PregnancyWeek: data.PregnancyWeek || 0,  // Now fetched from backend
        LastPeriodDate: data.LastPeriodDate || "N/A",
        ntValue: data.NuchalTranslucencyValue || "N/A",
      };
      this.$forceUpdate();
    } catch (error) {
      console.error("❌ Error fetching patient details:", error);
    }
  },
  methods: {
    logout() {
      sessionStorage.removeItem("barcode");
      alert("Logged out successfully!");
      this.$router.push("/"); // Redirect to login page
    },
  },
};
</script>


<style scoped>
.patient-screen {
  text-align: center;
  padding-top: 80px;
}

.tableau-iframe {
  width: 100%;
  height: 700px;
  border: none;
  margin-top: 20px;
}

.components-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Up to 3 components per row */
  gap: 20px; /* Spacing between components */
  justify-content: center;
  align-items: center;
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
}
</style>

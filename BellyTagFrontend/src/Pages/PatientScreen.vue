<template>
  <div class="patient-screen">
    <h1>Patient: {{ patient.username }}</h1>

    <!-- ✅ עטיפת הקומפוננטות ב-Grid -->
    <div class="components-grid">
      <PregnancyWeek :week="patient.pregnancyWeek" />
      <BloodTests />
      <LastPeriodDate :date="patient.lastPeriodDate" @update-date="updateLastPeriodDate" />
      <NuchalTranslucencySummary :nt-value="patient.ntValue" />
    </div>
  </div>
</template>

<script>
import logoImage from "@/Assets/logo.png";
import PregnancyWeek from "@/Components/PregnancyWeek.vue";
import BloodTests from "@/Components/BloodTests.vue";
import LastPeriodDate from "@/Components/LastPeriodDate.vue";
import NuchalTranslucencySummary from "@/Components/NuchalTranslucencySummary.vue"; // ✅ ייבוא הקומפוננטה החדשה

export default {
  components: {
    PregnancyWeek,
    BloodTests,
    LastPeriodDate,
    NuchalTranslucencySummary, // ✅ הוספת הקומפוננטה החדשה
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
      const patientId = this.$route.params.id;
      const apiUrl = `http://127.0.0.1:8080/patient/${patientId}`;
      const response = await fetch(apiUrl);
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      this.patient = await response.json();
    } catch (error) {
      console.error("❌ Error fetching patient details:", error);
    }
  },
  methods: {
    logout() {
      // Clear sessionStorage and redirect to login page
      sessionStorage.removeItem("barcode");
      alert("Logged out successfully!");
      this.$router.push("/"); // Redirect to login page
    },
    updateLastPeriodDate(newDate) {
      this.patient.lastPeriodDate = newDate; // Update the last period date in the parent component
      console.log("Updated Last Period Date:", newDate);
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

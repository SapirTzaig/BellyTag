<template>
  <div class="patient-screen">
    <h1>Patient: {{ patient.username }}</h1>

    <div class="components-grid">
      <PregnancyWeek :lastPeriodDate="patient.LastPeriodDate" />
      <LastPeriodDate :lastPeriodDate="patient.LastPeriodDate" @update-date="updateLastPeriodDate" />
      <NuchalTranslucencySummary :nt-value="patient.ntValue" />
      <NasalBoneSummary :nasalBone="patient.nasalBone" />
      <CheckList />
      <BloodTests />
      <GBSTest :gbsResult="patient.gbsResult" />
      <ScreeningAccuracy :falsePositiveRisk="patient.falsePositiveRisk" :falseNegativeRisk="patient.falseNegativeRisk" />
      <FollowUpTests :ultrasoundNeeded="patient.ultrasoundNeeded" :amniocentesisNeeded="patient.amniocentesisNeeded" />
      <AbnormalIndications :indications="patient.abnormalIndications" />


    </div>
  </div>
</template>

<script>
import logoImage from "@/Assets/logo.png";
import PregnancyWeek from "@/Components/PregnancyWeek.vue";
import BloodTests from "@/Components/BloodTests.vue";
import LastPeriodDate from "@/Components/LastPeriodDate.vue";
import NuchalTranslucencySummary from "@/Components/NuchalTranslucencySummary.vue";
import NasalBoneSummary from "@/Components/NasalBoneSummary.vue";
import CheckList from "@/Components/CheckList.vue";
import GBSTest from "@/Components/GBSTest.vue";
import ScreeningAccuracy from "@/Components/ScreeningAccuracy.vue";
import FollowUpTests from "@/Components/FollowUpTests.vue";
import AbnormalIndications from "@/Components/AbnormalIndications.vue";



export default {
  components: {
    PregnancyWeek,
    BloodTests,
    LastPeriodDate,
    NuchalTranslucencySummary,
    NasalBoneSummary,
    CheckList,
    GBSTest,
    ScreeningAccuracy,
    FollowUpTests,
    AbnormalIndications,
    

  },
  data() {
    return {
      patient: {},
      logoImage,
      barcode: sessionStorage.getItem("barcode") || "",
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
      const response = await fetch(`http://localhost:5000/personal?barcode=${patientId}`, {
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
        nasalBone: data.NasalBoneDetermination || false
      };
    } catch (error) {
      console.error("❌ Error fetching patient details:", error);
    }
  }
};
</script>

<style scoped>
.patient-screen {
  text-align: center;
  padding-top: 50px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.components-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
  max-width: 1200px;
  width: 100%;
  padding: 20px;
}

.component-item {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.pregnancy-week {
  grid-column: span 1;
}

.blood-tests {
  grid-column: span 1;
}

.last-period {
  grid-column: span 1;
}

.nuchal-translucency {
  grid-column: span 1;
}

.nasal-bone {
  grid-column: span 1;
  min-height: 150px;
}

.checklist {
  grid-column: span 2;
  width: 100%;
  min-height: 300px;
}


.normal {
  color: green;
  font-weight: bold;
}

.danger {
  color: red;
  font-weight: bold;
}
</style>

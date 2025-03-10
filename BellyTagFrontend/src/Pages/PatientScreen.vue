<template>
  <div class="patient-screen">
    <h1 class="patient-title">
      <span>Welcome,</span> {{ patient.username }} 💙
    </h1>
    <p class="subtitle">Your Pregnancy Dashboard</p>

    <div class="components-grid">
      <div class="grid-section">
        <h2>Pregnancy Overview</h2>
        <div class="grid-container pregnancy-grid">
          <PregnancyWeek :lastPeriodDate="patient.LastPeriodDate" />
          <LastPeriodDate :lastPeriodDate="patient.LastPeriodDate" @update-date="updateLastPeriodDate" />
          <NuchalTranslucencySummary :nt-value="patient.ntValue" :barcode="barcode" />
          <NasalBoneSummary :nasalBone="patient.nasalBone" />
        </div>
      </div>
      
      <div class="grid-section full-width">
        <CheckList />
      </div>

      <div class="grid-section">
        <h2>Laboratory Tests</h2>
        <div class="grid-container">
          <BloodTests />
          <GBSTest :gbsResult="patient.gbsResult" />
        </div>
      </div>

      <div class="grid-section">
        <h2>Follow-up & Risk Screening</h2>
        <div class="grid-container">
          <ScreeningAccuracy :falsePositiveRisk="patient.falsePositiveRisk" :falseNegativeRisk="patient.falseNegativeRisk" />
          <FollowUpTests :ultrasoundNeeded="patient.ultrasoundNeeded" :amniocentesisNeeded="patient.amniocentesisNeeded" />
          <AbnormalIndications :indications="patient.abnormalIndications" />
        </div>
      </div>
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
      barcode: this.$route.params.barcode,
    };
  },
  async created() {
    try {
      const patientId = sessionStorage.getItem('barcode');
      const response = await fetch(`http://localhost:5000/personal?barcode=${this.barcode}`, {
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
  width: 100%;
}

.components-grid {
  display: flex;
  flex-direction: column;
  gap: 30px;
  max-width: 1200px;
  width: 100%;
  padding: 20px;
}

/* 🔹 הפרדה בין קבוצות שונות של בדיקות */
.grid-section {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 🔹 עיצוב הכותרות */
.grid-section h2 {
  margin-bottom: 15px;
  color: #007bff;
  font-size: 1.4em;
}

/* 🔹 גריד פנימי לכל קבוצה */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

/* 🔹 שינוי הגריד של Pregnancy Overview ל-4 עמודות */
.pregnancy-grid {
  grid-template-columns: repeat(4, 1fr); /* 4 עמודות אחידות */
}

/* 🔹 הצ'קליסט יתפרס על כל הרוחב */
.full-width {
  grid-column: span 2;
}

/* 🔹 עיצוב אחיד לקומפוננטות */
.component-item {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 🎨 קביעת גדלים לפי תוכן */
.pregnancy-week, .last-period, .nuchal-translucency, .nasal-bone {
  grid-column: span 1;
}

/* 🎨 צבעים לתוצאות */
.normal {
  color: green;
  font-weight: bold;
}

.danger {
  color: red;
  font-weight: bold;
}

.patient-title {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  color: #007bff;
  margin-bottom: 5px;
}

.patient-title span {
  font-size: 24px;
  color: #2c3e50;
}

.subtitle {
  font-size: 18px;
  color: #555;
  text-align: center;
  margin-bottom: 20px;
  font-style: italic;
}

</style>

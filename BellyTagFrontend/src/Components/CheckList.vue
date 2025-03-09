<template>
    <div class="checklist-container">
      <h2>Pregnancy Check-Up Checklist</h2>
  
      <div class="checklist-grid">
        <!-- 🔹 טור לבדיקות חובה -->
        <div class="section mandatory">
          <h3>Mandatory Tests</h3>
          <ul>
            <li v-for="(test, index) in mandatoryTests" :key="'mandatory-' + index">
              <input type="checkbox" :id="'mandatory-' + index" v-model="completedTests[test]" @change="saveChecklist" />
              <label :for="'mandatory-' + index">{{ test }}</label>
            </li>
          </ul>
        </div>
  
        <!-- 🔹 טור לבדיקות מומלצות -->
        <div class="section recommended">
          <h3>Recommended Tests</h3>
          <ul>
            <li v-for="(test, index) in recommendedTests" :key="'recommended-' + index">
              <input type="checkbox" :id="'recommended-' + index" v-model="completedTests[test]" @change="saveChecklist" />
              <label :for="'recommended-' + index">{{ test }}</label>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        mandatoryTests: [
          "Blood Test",
          "Blood Type & Rh Factor",
          "Fasting Glucose Test",
          "Urine Test",
          "CMV, Toxoplasmosis & Rubella Tests",
          "HIV, Syphilis, Hepatitis B & C",
          "First Ultrasound (Nuchal Translucency)",
          "Alpha-Fetoprotein Test",
          "Glucose Tolerance Test (24-28 weeks)",
          "Early Anatomy Scan",
          "Late Anatomy Scan",
          "Glucose Tolerance Test (100g, if needed)",
          "Antibody Test (for Rh-negative women)",
          "Ultrasound for Weight & Placenta Check",
          "GBS Test (Group B Streptococcus)"
        ],
        recommendedTests: [
          "NIPT Genetic Test",
          "Third-trimester Anatomy Scan",
          "Fetal Echocardiography",
          "Fetal MRI",
          "Parental Genetic Carrier Screening",
          "Vitamin D & B12 Tests",
          "Fetal Heart Rate Monitoring (NST)"
        ],
        completedTests: {}
      };
    },
    mounted() {
      const savedChecklist = localStorage.getItem("pregnancyChecklist");
      if (savedChecklist) {
        this.completedTests = JSON.parse(savedChecklist);
      }
    },
    methods: {
      saveChecklist() {
        localStorage.setItem("pregnancyChecklist", JSON.stringify(this.completedTests));
      }
    }
  };
  </script>
  
  <style scoped>
  .checklist-container {
    width: 100%;
    max-width: 900px;
    margin: 20px auto;
    padding: 20px;
    background: #fdfbfb;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    font-family: Arial, sans-serif;
    text-align: center;
  }
  
  /* 🔹 עיצוב כותרות */
  h2 {
    color: #333;
    font-size: 24px;
    margin-bottom: 15px;
  }
  
  /* 🔹 פריסת הבדיקות בשני טורים */
  .checklist-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
    text-align: left;
  }
  
  /* 🔹 עיצוב כל טור */
  .section {
    padding: 15px;
    border-radius: 10px;
    background: white;
    box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  /* 🔹 הבדיקות החיוניות עם מסגרת כחולה */
  .mandatory {
    border-left: 5px solid #007bff;
  }
  
  /* 🔹 הבדיקות המומלצות עם מסגרת ירוקה */
  .recommended {
    border-left: 5px solid #28a745;
  }
  
  h3 {
    color: #007bff;
    font-size: 20px;
    margin-bottom: 10px;
  }
  
  /* 🔹 רשימות בדיקות */
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  /* 🔹 עיצוב של כל בדיקה ברשימה */
  li {
    display: flex;
    align-items: center;
    padding: 5px 0;
  }
  
  /* 🔹 צ'קבוקסים מוגדלים */
  input[type="checkbox"] {
    margin-right: 10px;
    transform: scale(1.3);
    cursor: pointer;
  }
  
  /* 🔹 עיצוב טקסט */
  label {
    cursor: pointer;
    font-size: 16px;
  }
  
  /* 🔹 התאמה לטלפונים - שני הטורים יהפכו לעמודה אחת */
  @media (max-width: 768px) {
    .checklist-grid {
      grid-template-columns: 1fr;
    }
  }
  </style>
  
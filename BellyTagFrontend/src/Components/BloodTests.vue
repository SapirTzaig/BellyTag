<template>
    <div class="blood-tests-container">
      <h2>Recent Blood Tests</h2>
  
      <!-- תפריט לבחירת בדיקה -->
      <select v-model="selectedTest" class="test-selection">
        <option value="">Select Test</option>
        <option v-for="test in tests" :key="test.name" :value="test.name">
          {{ test.name }}
        </option>
      </select>
  
      <!-- הצגת תוצאה רק אם נבחרה בדיקה -->
      <div v-if="selectedTest" class="test-result">
        <h3>{{ selectedTest }}</h3>
        <p>{{ getTestResult(selectedTest) }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedTest: "", // בדיקה נבחרת
        tests: [
          { name: "Ultrasound for Fetal Nuchal Translucency", result: "Normal measurement of 1.2mm" },
          { name: "Ultrasound for Fetal Nasal Bone Determination", result: "Nasal bone present, no abnormalities detected" },
          { name: "Maternal Serum (Blood) Tests", result: "Beta-hCG: 50,000 mIU/ml (Normal range)" },
          { name: "Genetic Screening Recommendation", result: "Recommended based on maternal age" },
          { name: "Multiple Marker Blood Tests (Second Trimester)", result: "AFP: 30 ng/ml, Estriol: Normal, hCG: Elevated" },
          { name: "Possible Abnormal Indications", result: "No abnormalities detected" },
          { name: "Follow-up Testing", result: "Further ultrasound recommended in 2 weeks" },
          { name: "Screening Accuracy", result: "99.5% accuracy for Down syndrome detection" },
          { name: "Group B Streptococcus Presence", result: "Negative result" },
        ],
      };
    },
    methods: {
      getTestResult(testName) {
        const test = this.tests.find((t) => t.name === testName);
        return test ? test.result : "No data available";
      },
    },
  };
  </script>
  
  <style scoped>
  .blood-tests-container {
    background: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    margin: 20px auto;
  }
  h2 {
    color: #333;
  }
  .test-selection {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  .test-result {
    margin-top: 20px;
    padding: 15px;
    background: #e3f2fd;
    border-radius: 5px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  h3 {
    color: #0277bd;
  }
  p {
    font-size: 16px;
    color: #555;
  }
  </style>
  
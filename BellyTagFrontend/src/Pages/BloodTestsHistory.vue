<template>
    <div class="history-container">
      <h2>Blood Test History</h2>
  
      <label>Select Previous Test:</label>
      <select v-model="selectedTestDate">
        <option v-for="test in bloodTestsHistory" :key="test.date" :value="test.date">
          {{ test.date }}
        </option>
      </select>
  
      <div class="tests-grid">
        <div class="test-card" v-for="test in selectedTestData" :key="test.name">
          <h3>{{ test.name }}</h3>
          <p><strong>Result:</strong> {{ test.value }}</p>
          <p><strong>Normal Range:</strong> {{ test.min }} - {{ test.max }}</p>
          <p :class="getStatusClass(test.value, test.min, test.max)">
            {{ getStatusText(test.value, test.min, test.max) }}
          </p>
        </div>
      </div>
  
      <button @click="$router.push('/')">Back to Main Page</button>
    </div>
  </template>
  
  <script>
  import bloodTestsData from "@/data/blood_tests_data.json"; // טעינת הנתונים מה-JSON
  
  export default {
    data() {
      return {
        selectedTestDate: bloodTestsData.latestTest.date, // הבדיקה הכי עדכנית
        bloodTestsHistory: bloodTestsData.history
      };
    },
    computed: {
      selectedTestData() {
        return this.bloodTestsHistory.find(test => test.date === this.selectedTestDate)?.tests || [];
      }
    },
    methods: {
      getStatusClass(value, min, max) {
        if (value < min || value > max) return "danger";
        return "normal";
      },
      getStatusText(value, min, max) {
        if (value < min) return "Below Normal";
        if (value > max) return "Above Normal";
        return "Within Normal Range";
      }
    }
  };
  </script>
  
  <style scoped>
  .history-container {
    max-width: 800px;
    margin: 20px auto;
    font-family: Arial, sans-serif;
    text-align: center;
  }
  
  .tests-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    margin-top: 10px;
  }
  
  .test-card {
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    text-align: center;
    border: 1px solid #ddd;
  }
  
  select {
    margin-top: 10px;
    padding: 5px;
  }
  </style>
  
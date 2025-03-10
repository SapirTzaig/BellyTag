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
      <div class="test-card" v-for="test in selectedTestData" :key="test.name" :style="{ backgroundColor: getCardColor(test.value, test.min, test.max) }">
        <h3>{{ test.name }}</h3>
        <p><strong>Result:</strong> {{ test.value }}</p>
        <p><strong>Normal Range:</strong> {{ test.min }} - {{ test.max }}</p>
        <p :class="getStatusClass(test.value, test.min, test.max)">
          {{ getStatusText(test.value, test.min, test.max) }}
        </p>
        <PieChart :value="test.value" :min="test.min" :max="test.max" />
      </div>
    </div>

    <button class="back-button" @click="$router.push(`/patient/${barcode}`)">Back to Main Page</button>
  </div>
</template>

<script>
import bloodTestsData from "@/Assets/blood_tests_data.json";
import PieChart from "@/Components/PieChart.vue"; 

export default {
  components: {
    PieChart
  },
  data() {
    return {
      barcode: "",
      selectedTestDate: bloodTestsData.latestTest.date,
      bloodTestsHistory: bloodTestsData.history
    };
  },
  computed: {
    selectedTestData() {
      return this.bloodTestsHistory.find(test => test.date === this.selectedTestDate)?.tests || [];
    }
  },
  mounted() {
    this.barcode = sessionStorage.getItem('barcode');
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
    },
    getCardColor(value, min, max) {
      if (value < min) return "#FFDDC1";
      if (value > max) return "#FFC1C1";
      return "#C1FFD7";
    }
  }
};
</script>

<style scoped>
.history-container {
  max-width: 900px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
  text-align: center;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.tests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.test-card {
  padding: 15px;
  border-radius: 12px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.test-card:hover {
  transform: scale(1.05);
}

select {
  margin-top: 10px;
  padding: 7px;
  border-radius: 6px;
  border: 1px solid #ddd;
}

button.back-button {
  margin-top: 20px;
  padding: 10px 15px;
  border: none;
  background: #007bff;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

button.back-button:hover {
  background: #0056b3;
}

.danger {
  color: red;
  font-weight: bold;
}

.normal {
  color: green;
  font-weight: bold;
}
</style>

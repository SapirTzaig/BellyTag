<template>
  <div class="blood-tests-container">
    <h2>Pregnancy Blood Tests</h2>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Test Name</th>
            <th>Result</th>
            <th>Normal Range</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="test in latestBloodTests" :key="test.name">
            <td>{{ test.name }}</td>
            <td>{{ test.value }}</td>
            <td>{{ test.min }} - {{ test.max }}</td>
            <td :class="getStatusClass(test.value, test.min, test.max)">
              {{ getStatusText(test.value, test.min, test.max) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <button @click="$router.push('/blood-tests-history')">View More Tests</button>
  </div>
</template>

<script>
import bloodTestsData from "@/Assets/blood_tests_data.json"; // טעינת הנתונים מה-JSON

export default {
  data() {
    return {
      latestBloodTests: bloodTestsData.latestTest.tests // הבדיקות האחרונות
    };
  },
  methods: {
    getStatusClass(value, min, max) {
      if (value < min || value > max) return "danger";
      if (value === min || value === max) return "warning";
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
.blood-tests-container {
  max-width: 700px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
  background: #f9f9f9;
  border: 2px solid #ccc;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  color: #333;
}

.table-wrapper {
  max-height: 250px;
  overflow-y: auto; /* גלילה אנכית */
  border: 1px solid #ddd;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: center;
  border: 1px solid #ddd;
}

th {
  background-color: #f4f4f4;
}

.normal {
  color: green;
}

.warning {
  color: orange;
}

.danger {
  color: red;
}

button {
  margin-top: 10px;
  padding: 10px 20px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>

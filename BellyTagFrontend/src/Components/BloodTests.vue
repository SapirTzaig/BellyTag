<template>
  <div class="blood-tests-container">
    <h2>🩸 Pregnancy Blood Tests</h2>
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
            <td>
              <span :class="getStatusClass(test.value, test.min, test.max)">
                {{ getStatusText(test.value, test.min, test.max) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <button @click="$router.push('/blood-tests-history')">View More Tests</button>
  </div>
</template>

<script>
import bloodTestsData from "@/Assets/blood_tests_data.json";

export default {
  data() {
    return {
      latestBloodTests: bloodTestsData.latestTest.tests
    };
  },
  methods: {
    getStatusClass(value, min, max) {
      if (value < min) return "danger";
      if (value > max) return "danger";
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
/* 🎨 עיצוב כללי */
.blood-tests-container {
  max-width: 800px;
  margin: 20px auto;
  font-family: "Inter", sans-serif;
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: 0.3s ease-in-out;
}

/* 🎨 כותרת */
h2 {
  color: #333;
  font-size: 24px;
  margin-bottom: 15px;
}

/* 📜 עיצוב טבלה מודרנית */
.table-wrapper {
  max-height: 300px;
  overflow-y: auto;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 12px;
}

th {
  background: #007bff;
  color: white;
  padding: 12px;
  font-size: 16px;
  text-align: center;
  border-radius: 12px 12px 0 0;
}

td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #f1f1f1;
}

/* 🔹 אפקט מעבר על שורות */
tbody tr:hover {
  background: rgba(0, 123, 255, 0.05);
}

/* 🎨 תגיות סטטוס */
.normal {
  background-color: #e3fcef;
  color: #2e7d32;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: bold;
  display: inline-block;
}

.warning {
  background-color: #fff4e5;
  color: #b9770e;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: bold;
  display: inline-block;
}

.danger {
  background-color: #fde8e8;
  color: #c0392b;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: bold;
  display: inline-block;
}

/* 🖱️ כפתור מודרני */
button {
  margin-top: 20px;
  padding: 12px 20px;
  background: #007bff;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 4px 6px rgba(0, 123, 255, 0.2);
}

button:hover {
  background: #0056b3;
  box-shadow: 0 6px 12px rgba(0, 123, 255, 0.3);
  transform: translateY(-2px);
}

@media (prefers-color-scheme: dark) {
  .blood-tests-container {
    background: #222;
    color: white;
  }

  table {
    background: #333;
  }

  th {
    background: #0056b3;
  }

  td {
    border-bottom: 1px solid #444;
  }

  .table-wrapper {
    box-shadow: 0 2px 6px rgba(255, 255, 255, 0.1);
  }

  button {
    background: #0056b3;
  }

  button:hover {
    background: #003d80;
  }
}
</style>

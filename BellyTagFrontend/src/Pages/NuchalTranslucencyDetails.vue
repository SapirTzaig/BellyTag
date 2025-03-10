<template>
  <div class="nt-details-container">
    <h2>Nuchal Translucency Screening - Detailed Report</h2>

    <table class="nt-table">
      <thead>
        <tr>
          <th>Week</th>
          <th>NT (mm)</th>
          <th>CRL (mm)</th>
          <th>BPD (mm)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ ntTest.week }}</td>
          <td>{{ ntTest.nt }}</td>
          <td>{{ ntTest.crl }}</td>
          <td>{{ ntTest.bpd }}</td>
        </tr>
      </tbody>
    </table>

    <button @click="goBack">Back</button>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

export default defineComponent({
  setup() {
    const router = useRouter();
    const route = useRoute(); // Get the current route
    const ntTest = ref({ week: "", nt: "", crl: "", bpd: "" });

    // Get barcode from query parameters
    const patientId = route.query.barcode;

    const fetchData = async () => {
      try {
        if (!patientId) {
          console.error("No patient barcode found in query parameters");
          return;
        }

        // Fetch pregnancy start week
        const personalResponse = await fetch(`http://localhost:5000/personal?barcode=${patientId}`, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });

        if (!personalResponse.ok) throw new Error(`HTTP error! Status: ${personalResponse.status}`);

        const personalData = await personalResponse.json();
        const last_period = new Date(personalData.LastPeriodDate);

        // Fetch test data using query parameters (corrected GET request)
        const testResponse = await fetch(
          `http://localhost:5000/test?barcode=${patientId}&testName=Ultrasound%20for%20Fetal%20Nuchal%20Translucency`,
          {
            method: "GET",
            headers: { "Content-Type": "application/json" },
          }
        );

        if (!testResponse.ok) throw new Error(`HTTP error! Status: ${testResponse.status}`);

        const testData = await testResponse.json();
        const latestTest = testData.latestTest;
        const testDate = new Date(latestTest.date);
        const currentWeek = Math.floor((testDate - last_period) / (7 * 24 * 60 * 60 * 1000));

        // Extract relevant attributes
        const attributes = { nt: "", crl: "", bpd: "" };
        latestTest.attributes.forEach(attr => {
          if (attr.name === "Nuchal Translucency") attributes.nt = attr.value;
          if (attr.name === "Crown Rump Length") attributes.crl = attr.value;
          if (attr.name === "Biparietal diameter") attributes.bpd = attr.value;
        });

        ntTest.value = { week: `Week ${currentWeek}`, ...attributes };
      } catch (error) {
        console.error("Error fetching test data:", error);
      }
    };

    onMounted(fetchData);

    // Navigate back and pass the barcode
    const goBack = () => {
      router.push({ path: `/patient/${patientId}`, query: { barcode: patientId } });
    };

    return { ntTest, goBack };
  },
});
</script>

<style scoped>
.nt-details-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nt-table {
  width: 80%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.nt-table th,
.nt-table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.nt-table th {
  background-color: #f4f4f4;
}

button {
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>

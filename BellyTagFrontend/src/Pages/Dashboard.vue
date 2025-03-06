<template>
  <div class="dashboard">
    <h1>Doctor Dashboard</h1>
    
    <!-- Display list of patients -->
    <h2>Patients List</h2>
    <ul>
      <li
        v-for="(patient, index) in patients"
        :key="patient.id"
        @click="selectPatient(patient.id)"
        class="patient-item"
      >
        {{ patient.name }}
      </li>
    </ul>

    <!-- Patient Data Search -->
    <input
      v-model="patientId"
      placeholder="Enter Patient ID"
      @keyup.enter="fetchPatientData"
    />
    <button @click="fetchPatientData">Fetch Patient Data</button>
    
    <!-- Display Patient Data and Alerts -->
    <div v-if="patientData">
      <h2>Patient Information</h2>
      <p><strong>Name:</strong> {{ patientData.name }}</p>
      <p><strong>Age:</strong> {{ patientData.age }}</p>
      <p><strong>Previous Labors:</strong> {{ patientData.previous_labors }}</p>
      <p><strong>Risk Pregnancy:</strong> {{ patientData.risk_pregnancy }}</p>
      
      <!-- Display Alerts if any -->
      <div v-if="patientData.alerts && patientData.alerts.length > 0">
        <h3>Alerts:</h3>
        <ul>
          <li v-for="(alert, index) in patientData.alerts" :key="index">{{ alert }}</li>
        </ul>
      </div>

      <!-- Display Medical Tests -->
      <h3>Medical Tests:</h3>
      <ul>
        <li v-for="(test, index) in patientData.tests" :key="index">
          <strong>{{ test.test_name }}:</strong> {{ test.test_result }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      patientId: "",
      patients: [], // List of patients
      patientData: null,
      barcode: sessionStorage.getItem("barcode") || "", // Barcode from sessionStorage
    };
  },
  methods: {
    // Fetch all patients for the doctor
    async fetchPatients() {
      const response = await fetch("http://localhost:5000/doctor/patients", {
        method: "GET",
      });
      const result = await response.json();
      if (response.ok) {
        this.patients = result.patients; // Populate the patient list
      } else {
        alert(result.message);
      }
    },

    // Fetch specific patient data
    async fetchPatientData() {
      if (!this.patientId) {
        alert("Please enter a patient ID.");
        return;
      }

      const response = await fetch(
        `http://localhost:5000/doctor/view_patient/${this.patientId}`,
        { method: "GET" }
      );

      const result = await response.json();
      if (response.ok) {
        this.patientData = result.patient_data;
      } else {
        alert(result.message);
      }
    },

    // Select a patient from the list to view more details
    selectPatient(patientId) {
      this.patientId = patientId;
      this.fetchPatientData(); // Fetch data for the selected patient
    },

    // Logout and clear sessionStorage
    logout() {
      sessionStorage.clear(); // Clear sessionStorage when logging out
      alert("Logged out successfully!");
      this.$router.push("/"); // Redirect to the login page
    },
  },
  created() {
    // Check if the doctor's barcode is stored in sessionStorage
    const doctorBarcode = sessionStorage.getItem("barcode");
    if (!doctorBarcode) {
      this.$router.push("/"); // If not, redirect to login page
    } else {
      this.barcode = doctorBarcode; // Set the barcode from sessionStorage
    }
  },
};
</script>

<style scoped>
.dashboard {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

input {
  padding: 10px;
  width: 100%;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px;
  background-color: #4caf50;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

h3 {
  margin-top: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
  cursor: pointer;
}

li:hover {
  background-color: #f0f0f0;
  border-radius: 4px;
}

.patient-item {
  cursor: pointer;
}
</style>

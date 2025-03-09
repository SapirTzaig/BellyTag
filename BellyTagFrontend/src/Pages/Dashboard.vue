<template>
  <div class="dashboard">
    <h1>Doctor Dashboard</h1>

    <!-- Patient Barcode Input -->
    <input
      v-model="patientBarcode"
      placeholder="Enter Patient Barcode"
      @keyup.enter="fetchPatientData"
    />
    <button @click="fetchPatientData">Search Patient</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      patientBarcode: "",
    };
  },
  methods: {
    async fetchPatientData() {
      if (!this.patientBarcode) {
        alert("Please enter a patient barcode.");
        return;
      }

      try {
        const response = await fetch("http://localhost:5000/check_patient", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ barcode: this.patientBarcode }),
        });

        const result = await response.json();

        if (response.ok && result.exists) {
          // Store patient barcode in sessionStorage
          sessionStorage.setItem("patientBarcode", this.patientBarcode);
          
          // Redirect to patient screen
          this.$router.push(`/Doctor_patient/${this.patientBarcode}`);
        } else {
          alert("No patient found with this barcode.");
        }
      } catch (error) {
        alert("An error occurred while searching for the patient.");
      }
    },

    logout() {
      sessionStorage.clear();
      alert("Logged out successfully!");
      this.$router.push("/");
    },
  },
  created() {
    const doctorBarcode = sessionStorage.getItem("barcode");
    const role = sessionStorage.getItem("role");

    if (!doctorBarcode || role !== "doctor") {
      this.$router.push("/");
    }
  },
};
</script>

<style scoped>
.dashboard {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  text-align: center;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
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
</style>

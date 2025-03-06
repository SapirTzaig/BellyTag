<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="onRegister">
      <!-- Your form fields here -->
      <div class="form-group">
        <label>First Name:</label>
        <input type="text" v-model="form.firstName" required />
      </div>
      <div class="form-group">
        <label>Last Name:</label>
        <input type="text" v-model="form.lastName" required />
      </div>
      <div class="form-group">
        <label>ID:</label>
        <input type="text" v-model="form.id" required />
      </div>
      <div class="form-group">
        <label>Date of Birth:</label>
        <input type="date" v-model="form.dob" @change="calculateAge" required />
      </div>
      <div class="form-group">
        <label>Age:</label>
        <input type="number" v-model="form.age" readonly />
      </div>
      <div class="form-group">
        <label>Gender:</label>
        <div class="gender-group">
          <input type="radio" id="male" value="Male" v-model="form.gender" required />
          <label for="male">Male</label>
          <input type="radio" id="female" value="Female" v-model="form.gender" required />
          <label for="female">Female</label>
        </div>
      </div>
      <div class="form-group">
        <label>Status:</label>
        <select v-model="form.status" required>
          <option value="">Select</option>
          <option value="Single">Single</option>
          <option value="Married">Married</option>
        </select>
      </div>
      <div v-if="form.status === 'Married'" class="form-group">
        <label>Number of Children:</label>
        <input type="number" v-model="form.children" min="0" />
      </div>
      <div class="form-group">
        <label>Email:</label>
        <input type="email" v-model="form.email" required />
      </div>
      <div class="form-group">
        <label>Password:</label>
        <input type="password" v-model="form.password" required />
      </div>
      <div class="form-group">
        <label>Role:</label>
        <div class="role-group">
          <input type="radio" id="doctor" value="Doctor" v-model="form.role" required />
          <label for="doctor">Doctor</label>
          <input type="radio" id="patient" value="Patient" v-model="form.role" required />
          <label for="patient">Patient</label>
        </div>
      </div>
      <div v-if="form.role === 'Doctor'" class="form-group">
        <label>Doctor License Number:</label>
        <input type="text" v-model="form.license" required />
      </div>
      <!-- Show only if the user is a Patient -->
      <div v-if="form.role === 'Patient'" class="form-group">
        <label>Date of Last Period:</label>
        <input type="date" v-model="form.lastPeriod" />
      </div>
      <div class="buttons">
        <button type="button" class="reset-btn" @click="onReset">Reset</button>
        <button type="submit" :disabled="!isFormValid" class="submit-btn">Submit</button>
      </div>
    </form>
  </div>

  <!-- Alert and Download Button -->
  <div v-if="showAlert" class="custom-alert" :class="alertType">
    <p>{{ alertMessage }}</p>
    <div class="button-group">
      <button @click="closeAlert" class="small-btn">OK</button>
      <button v-if="showDownloadButton" @click="downloadBarcode" class="small-btn">Download Barcode</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        firstName: "",
        lastName: "",
        id: "",
        dob: "",
        age: "",
        gender: "",
        status: "",
        children: "",
        email: "",
        password: "",
        role: "",
        license: null,
        lastPeriod: null,
      },
      showAlert: false,
      showDownloadButton: false, // Control visibility of download button
      alertMessage: "",
      alertType: "",
      barcode: "", // Store the barcode
    };
  },
  computed: {
    isFormValid() {
      return (
        this.form.firstName &&
        this.form.lastName &&
        this.form.id &&
        this.form.dob &&
        this.form.age &&
        this.form.gender &&
        this.form.status &&
        this.form.email &&
        this.form.password &&
        this.form.role &&
        (this.form.role === "Doctor" ? this.form.license : true)
      );
    }
  },
  methods: {
    calculateAge() {
      if (this.form.dob) {
        const birthDate = new Date(this.form.dob);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
          age--;
        }
        this.form.age = age;
      }
    },

    async onRegister() {
      if (!this.isFormValid) return;

      const formToSend = {
        ...this.form,
        license: this.form.role === "Doctor" ? this.form.license : null,
        lastPeriod: this.form.role === "Doctor" ? null : this.form.lastPeriod,
      };

      try {
        const response = await fetch("http://localhost:5000/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formToSend),
        });

        const data = await response.json();

        if (response.ok && data.barcode) {
          this.barcode = data.barcode; // Store the barcode
          this.alertMessage = `Successfully registered! Your personal barcode is: ${data.barcode}. \nPlease keep it safe as you will not be able to retrieve your password!`;
          this.alertType = "success";
          this.showAlert = true;
          this.showDownloadButton = true; // Show download button
        } else {
          this.alertMessage = "Registration failed. Please try again.";
          this.alertType = "error";
          this.showAlert = true;
        }
      } catch (error) {
        this.alertMessage = "An error occurred. Please check your connection and try again.";
        this.alertType = "error";
        this.showAlert = true;
      }
    },

    closeAlert() {
      this.showAlert = false;
      if (this.alertType === "success") {
        this.$router.push("/");
      }
    },

    downloadBarcode() {
      const blob = new Blob([`Your barcode: ${this.barcode}`], { type: 'text/plain' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'barcode.txt';
      link.click();
    },

    onReset() {
      this.form = {
        firstName: "",
        lastName: "",
        id: "",
        dob: "",
        age: "",
        gender: "",
        status: "",
        children: "",
        email: "",
        password: "",
        role: "",
        license: null,
        lastPeriod: null,
        pregnancyWeek: null
      };
    }
  }
};
</script>

<style scoped>
.register-container {
  width: 400px;
  margin: auto;
  padding: 20px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.form-group {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  width: 40%; /* Align label with inputs */
}

input, select {
  width: 55%; /* Adjust width to make it uniform */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.gender-group, .role-group {
  display: flex;
  gap: 10px;
}

.buttons {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 10px;
  width: 30%;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-btn {
  background: #28a745;
  color: white;
}

.submit-btn:disabled {
  background: gray;
  cursor: not-allowed;
}

.reset-btn {
  background: #dc3545;
  color: white;
}

.custom-alert {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px;
  border-radius: 5px;
  font-weight: bold;
  z-index: 1000;
}

.custom-alert.success {
  background: #28a745;
  color: white;
}

.custom-alert.error {
  background: #dc3545;
  color: white;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 30px; /* Increased space between OK and Download Barcode buttons */
}

.small-btn {
  padding: 6px 12px;
  font-size: 14px;
}
</style>

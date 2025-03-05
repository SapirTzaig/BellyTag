<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="onRegister">
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

      <div class="buttons">
        <button type="button" class="reset-btn" @click="onReset">Reset</button>
        <button type="submit" :disabled="!isFormValid" class="submit-btn">Submit</button>
      </div>
    </form>
  </div>

  <div v-if="showAlert" class="custom-alert" :class="alertType">
    {{ alertMessage }}
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
        license: null, // Added license number for doctors
      },
      showAlert: false,
      alertMessage: "",
      alertType: "",
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
        this.form.role && // Ensure role is selected
        (this.form.role === "Doctor" ? this.form.license : true) // Validate license if role is doctor
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

      // Set the license number to null if the role is not Doctor
      const formToSend = {
        ...this.form,
        license: this.form.role === "Doctor" ? this.form.license : null,
      };

      try {
        const response = await fetch("http://your-server.com/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formToSend)
        });

        const data = await response.json();

        if (data.status === "ok" && data.barcode) {
          this.alertMessage = `Successfully registered! Your personal barcode is: ${data.barcode}`;
          this.alertType = "success";
          this.showAlert = true;
          setTimeout(() => {
            this.$router.push(`/login}`);
          }, 2000);
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
  width: 48%;
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

/* Align the alert message */
.custom-alert {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 15px;
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

</style>

<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input
        type="text"
        v-model="barcode"
        placeholder="Barcode"
        required
      />
      <input
        type="password"
        v-model="password"
        placeholder="Password"
        required
      />
      <button type="submit">Login</button>
      <div class="mt-2">
        Do not have an account yet?
        <router-link to="/register"> Register here</router-link>
        <router-link :to="`/upload/${barcode}`"> Upload here</router-link>
        <router-link :to="`/patient/ee78c1c2b2`"> Patient screen here</router-link>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      barcode: "",
      password: "",
    };
  },

  methods: {
    async login() {
      try {
        const response = await fetch("http://localhost:5000/login", { // Adjust URL for your local server
          method: "POST", // POST is more appropriate for sending data like password
          headers: {
            "Content-Type": "application/json", // Ensure the server knows the body is JSON
          },
          body: JSON.stringify({
            barcode: this.barcode, // Send barcode and password
            password: this.password,
          }),
        });

        const result = await response.json();
        console.log(result);
        if (response.ok) {
          // If login is successful, store the barcode in sessionStorage
          sessionStorage.setItem('barcode', this.barcode);

          // If user is a doctor, redirect to the dashboard
          if (result.role === "doctor") {
            this.$router.push("/dashboard");
            sessionStorage.setItem('role', this.role);
          } else if (result.role === "patient") {
            // If user is a patient, redirect to their personal screen
            this.$router.push(`/patient/${this.barcode}`);
            sessionStorage.setItem('role', this.role);
          }
        } else {
          alert(result.message || "Login failed. Please try again.");
        }
      } catch (error) {
        alert("An error occurred. Please check your connection and try again.");
      }
    },
  },
};
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

input {
  width: 80%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 60%;
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

.mt-2 {
  margin-top: 10px;
}
</style>

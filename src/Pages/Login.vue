<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input
        type="text"
        v-model="username"
        placeholder="Username"
        required
      />
      <input
      
        type="password"
        v-model="password"
        placeholder="Password"
        required
      />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      });

      const result = await response.json();

      if (response.ok) {
        // If login is successful, check the user's role
        if (result.role === "doctor") {
          // Redirect doctor to the dashboard
          this.$router.push("/dashboard");
        } else if (result.role === "patient") {
          // Redirect patient to their personal screen
          this.$router.push(`/patient/${result.id}`);
        }
      } else {
        alert(result.message || "Login failed. Please try again.");
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
  width: 80%;
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

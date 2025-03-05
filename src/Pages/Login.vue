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
      <div class="mt-2">
        Do not have an account yet?
        <router-link to="/register"> Register here</router-link>
      </div>
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
    login() {
      // Mock response
      const response = {
        ok: true,
        json: async () => ({
          id: 1,
          role: "patient",
          message: "Login successful",
        }),
      };

      response.json().then(result => {
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
      });
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
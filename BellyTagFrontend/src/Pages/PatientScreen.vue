<template>
  <div class="patient-screen">
    <nav class="navbar">
      <div class="nav-left">
        <img :src="logoImage" alt="Logo" class="logo" />
        <ul class="nav-links">
          <li><router-link to="/user-details">User Details</router-link></li>
          <li><router-link to="/upload">Upload File</router-link></li>
        </ul>
      </div>
      <a href="#" @click="logout" class="logout-button">Log Out</a>
    </nav>

    <h1>Patient: {{ patient.username || "Loading..." }}</h1>

    <!-- ✅ הצגת הדוח באמצעות iframe -->
    <iframe :src="tableauURL" class="tableau-iframe"></iframe>
  </div>
</template>

<script>
import logoImage from "@/Assets/logo.png";

export default {
  data() {
    return {
      patient: {},
      logoImage,
      tableauURL:
        "https://public.tableau.com/shared/37ZW4WCT6?:display_count=n&:origin=viz_share_link"
    };
  },
  async created() {
    try {
      const patientId = this.$route.params.id;
      const apiUrl = `http://127.0.0.1:8080/patient/${patientId}`;
      const response = await fetch(apiUrl);
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      this.patient = await response.json();
    } catch (error) {
      console.error("❌ Error fetching patient details:", error);
    }
  },
  methods: {
    logout() {
      alert("Logged out successfully!");
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
.patient-screen {
  text-align: center;
  padding-top: 80px;
}

.navbar {
  background-color: #acd2e7;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.logo {
  height: 40px;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 20px;
  margin: 0;
  padding: 0;
}

.nav-links li a {
  text-decoration: none;
  color: white;
  font-weight: bold;
}

.logout-button {
  text-decoration: none;
  color: white;
  font-weight: bold;
  padding: 10px 40px;
}

.tableau-iframe {
  width: 100%;
  height: 700px;
  border: none;
  margin-top: 20px;
}
</style>

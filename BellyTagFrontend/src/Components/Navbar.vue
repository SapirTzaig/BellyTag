<template>
  <div class="navbar">
    <div class="nav-left">
      <img :src="logoImage" alt="Logo" class="logo" />
      <ul class="nav-links">
        <li v-if="userRole === 'doctor'">
          <router-link to="/dashboard">Select Patient</router-link>
        </li>
        <li v-if="userRole === 'patient'">
          <router-link :to="`/patient/${barcode}`">Medical Status</router-link>
        </li>
        <li><router-link to="/user-details">User Details</router-link></li>
        <li v-if="userRole === 'patient'">
          <router-link :to="`/upload/${barcode}`">Upload File</router-link>
        </li>
      </ul>
    </div>
    <a href="#" @click="logout" class="logout-button">Log Out</a>
  </div>
</template>

<script>
export default {
  data() {
    return {
      logoImage,
      barcode: sessionStorage.getItem("barcode") || "",
      userRole: sessionStorage.getItem("role") || "",
    };
  },
  methods: {
    logout() {
      sessionStorage.clear();
      alert("Logged out successfully!");
      this.$router.push("/");
    },
    setFavicon() {
      let link = document.querySelector("link[rel~='icon']");
      if (!link) {
        link = document.createElement("link");
        link.rel = "icon";
        document.head.appendChild(link);
      }
      link.href = "./BellyTagFrontend/src/Assets/docho.ico"; // Use the file in the public folder
    },
  },
  mounted() {
    this.setFavicon(); // Set favicon when the component loads
  },
};
</script>

  
  <style scoped>
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
  </style>
  
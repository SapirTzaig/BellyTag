<template>
    <div class="navbar">
      <div class="nav-left">
        <img :src="logoImage" alt="Logo" class="logo" />
        <ul class="nav-links">
          <li v-if="userRole === 'doctor'">
          <router-link to="/dashboard">Main</router-link>
        </li>
        <li v-if="userRole === 'patient'">
          <router-link :to="`/patient/${barcode}`">Main</router-link>
        </li>
          <li><router-link to="/user-details">User Details</router-link></li>
          <li><router-link :to="`/upload/${barcode}`">Upload File</router-link></li>
        </ul>
      </div>
      <a href="#" @click="logout" class="logout-button">Log Out</a>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        logoImage: "@/Assets/logo.png", // Ensure the logo image is properly imported
        barcode: sessionStorage.getItem("barcode") || "", // Barcode from sessionStorage
        userRole: sessionStorage.getItem("role") || "", // Get user role from sessionStorage (doctor or patient)
      };
    },
    
    methods: {
      // Logout and clear sessionStorage
      logout() {
        sessionStorage.clear(); // Clear sessionStorage when logging out
        alert("Logged out successfully!");
        this.$router.push("/"); // Redirect to the login page
      },
    },
    computed: {
      isDoctor() {
        return sessionStorage.getItem('role') === 'doctor';
      },
      isPatient() {
        return sessionStorage.getItem('role') === 'patient';
      }
    }
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
  
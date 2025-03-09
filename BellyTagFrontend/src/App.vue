<template>
  <div id="app">
    <!-- Conditionally render the navbar based on route -->
    <navbar v-if="showNavbar" />
    
    <!-- The main content -->
    <router-view></router-view>
  </div>
</template>

<script>
import Navbar from "@/Components/Navbar.vue"; // Assuming Navbar is a separate component

export default {
  name: "App",
  components: {
    Navbar,
  },
  mounted() {
  this.userRole = sessionStorage.getItem("role");
  this.barcode = sessionStorage.getItem("barcode");
  },
  computed: {
    showNavbar() {
      // Check if the current route is 'login' or 'register'
      return this.$route.name !== 'login' && this.$route.name !== 'register';
    },
  },
};
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

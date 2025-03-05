<template>
    <div class="user-details">
      <h1>User Details</h1>
      <div v-if="user">
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Email:</strong> {{ user.mail }}</p>
        <p><strong>Age:</strong> {{ user.age }}</p>
        <p><strong>Gender:</strong> {{ user.gender }}</p>
        <p><strong>Status:</strong> {{ user.status }}</p>
        <p><strong>Date of Birth:</strong> {{ user.date_of_birth }}</p>
      </div>
      <div v-else>
        <p>Loading user details...</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        user: null
      };
    },
    async created() {
      try {
        const response = await fetch('http://localhost:5000/user'); // עדכן את ה-API בהתאם לשרת שלך
        const data = await response.json();
        this.user = data;
      } catch (error) {
        console.error("Error fetching user details:", error);
      }
    }
  };
  </script>
  
  <style scoped>
  .user-details {
    text-align: center;
    padding: 20px;
    max-width: 500px;
    margin: 0 auto;
    background: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  h1 {
    color: #2c3e50;
  }
  
  p {
    font-size: 18px;
    color: #333;
    margin: 10px 0;
  }
  </style>
  
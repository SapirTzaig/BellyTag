<template>
  <div class="patient-screen">
    <!-- NavBar -->
    <nav class="navbar">
      <ul>
        <li><router-link to="/user-details">User Details</router-link></li>
        <li><router-link to="/upload">Upload File</router-link></li>
        <li><a href="#" @click="logout">Log Out</a></li>
      </ul>
    </nav>

    <!-- תוכן הדף -->
    <h1>Patient: {{ patient.username }}</h1>
    <!-- הצגת מידע נוסף על המטופל -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      patient: {}
    };
  },
  async created() {
    const patientId = this.$route.params.id;
    const response = await fetch('http://localhost:5000/patient/' + patientId);
    const data = await response.json();
    this.patient = data;
  },
  methods: {
    logout() {
      // הוספת לוגיקה להתנתקות (למשל מחיקת טוקן ואיתחול דף)
      alert("Logged out successfully!");
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
/* עיצוב ה-NavBar */
.navbar {
  background-color: #2c3e50;
  padding: 10px;
  display: flex;
  justify-content: center;
}

.navbar ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
}

.navbar ul li {
  margin: 0 15px;
}

.navbar ul li a {
  text-decoration: none;
  color: white;
  font-weight: bold;
}

.navbar ul li a:hover {
  color: #f39c12;
}

.patient-screen {
  text-align: center;
  padding: 20px;
}
</style>
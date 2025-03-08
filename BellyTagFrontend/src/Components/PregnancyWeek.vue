<template>
  <div class="pregnancy-week-card">
    <h2>Pregnancy Week</h2>
    <p v-if="pregnancyWeek !== null">{{ pregnancyWeek }} Weeks</p>
    <p v-else class="default-text">Estimated Week: {{ defaultPregnancyWeek }} Weeks</p>
  </div>
</template>

<script>
export default {
  props: ["lastPeriodDate"], // Receives the last period date from the system
  computed: {
    pregnancyWeek() {
      if (!this.lastPeriodDate) return null; // If no last period date, return null
      const lastPeriod = new Date(this.lastPeriodDate);
      const today = new Date();
      const diffInDays = (today - lastPeriod) / (1000 * 60 * 60 * 24); // Calculate the difference in days
      return Math.floor(diffInDays / 7); // Divide by 7 to get the pregnancy week
    },
    defaultPregnancyWeek() {
      // Default value if there is no date: show estimated week as 0
      return 0;
    },
  },
};
</script>

<style scoped>
.pregnancy-week-card {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 250px;
  margin: 20px auto;
}
h2 {
  color: #333;
}
p {
  font-size: 20px;
  font-weight: bold;
  color: #4CAF50;
}
.default-text {
  color: #f39c12; /* Orange color to highlight estimated week */
  font-size: 18px;
  font-weight: bold;
}
</style>

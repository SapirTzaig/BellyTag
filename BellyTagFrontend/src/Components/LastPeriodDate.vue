<template>
  <div class="last-period-card">
    <h2>📅 Last Period Date</h2>
    <p class="date-text">{{ formattedDate }}</p>
  </div>
</template>

<script>
export default {
  props: ["lastPeriodDate"],
  computed: {
    formattedDate() {
      return this.lastPeriodDate
        ? new Date(this.lastPeriodDate).toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
          })
        : "N/A";
    },
  },
};
</script>

<style scoped>
.last-period-card {
  background: linear-gradient(to bottom, #fdfbfb, #f8f9fa); /* Gradient רקע עדין */
  padding: 20px;
  border-radius: 12px; /* פינות מעוגלות */
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 280px;
  margin: 20px auto;
  transition: transform 0.3s ease-in-out;
}

.last-period-card:hover {
  transform: scale(1.05); /* אפקט עדין בעת ריחוף */
}

h2 {
  color: #333;
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
}

.date-text {
  font-size: 20px;
  font-weight: bold;
  color: #4CAF50; /* ירוק */
}
</style>

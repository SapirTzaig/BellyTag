<template>
  <div class="pregnancy-week-card">
    <h2>🤰 Pregnancy Week</h2>
    <p v-if="pregnancyWeek !== null" class="week-text">
      <span class="week-number">{{ pregnancyWeek }}</span> Weeks
    </p>
    <p v-else class="default-text">
      Estimated Week: <span class="week-number">{{ defaultPregnancyWeek }}</span> Weeks
    </p>
  </div>
</template>

<script>
export default {
  props: ["lastPeriodDate"],
  computed: {
    pregnancyWeek() {
      if (!this.lastPeriodDate) return null;
      const lastPeriod = new Date(this.lastPeriodDate);
      const today = new Date();
      const diffInDays = (today - lastPeriod) / (1000 * 60 * 60 * 24);
      return Math.floor(diffInDays / 7);
    },
    defaultPregnancyWeek() {
      return 0;
    }
  }
};
</script>

<style scoped>
.pregnancy-week-card {
  background: linear-gradient(to bottom, #fdfbfb, #f8f9fa); 
  padding: 20px;
  border-radius: 12px; 
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 280px;
  margin: 20px auto;
  transition: transform 0.3s ease-in-out;
}

.pregnancy-week-card:hover {
  transform: scale(1.05); 
}

h2 {
  color: #333;
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
}

.week-text {
  font-size: 20px;
  font-weight: bold;
  color: #4CAF50; 
}

.default-text {
  color: #f39c12; 
  font-size: 18px;
  font-weight: bold;
}

.week-number {
  font-size: 28px;
  font-weight: bold;
  color: #2c3e50; 
}
</style>

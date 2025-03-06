<template>
  <div class="pregnancy-week-card">
    <h2>Pregnancy Week</h2>
    <p v-if="pregnancyWeek !== null">{{ pregnancyWeek }} Weeks</p>
    <p v-else class="default-text">Estimated Week: {{ defaultPregnancyWeek }} Weeks</p>
  </div>
</template>

<script>
export default {
  props: ["lastPeriodDate"], // מקבלת תאריך וסת אחרון מהמערכת
  computed: {
    pregnancyWeek() {
      if (!this.lastPeriodDate) return null; // אם אין תאריך וסת אחרון, נחזיר null
      const lastPeriod = new Date(this.lastPeriodDate);
      const today = new Date();
      const diffInDays = (today - lastPeriod) / (1000 * 60 * 60 * 24); // מחשבים מספר ימים
      return Math.floor(diffInDays / 7); // מחלקים ל-7 כדי לקבל שבועות
    },
    defaultPregnancyWeek() {
      // ברירת מחדל - אם אין נתון, נציג שהמטופלת בשבוע 8
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
  color: #f39c12; /* צבע כתום כדי להבליט שזה ערך משוער */
  font-size: 18px;
  font-weight: bold;
}
</style>

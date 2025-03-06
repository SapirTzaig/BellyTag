<template>
    <div class="last-period-container">
      <h2>Last Period Date</h2>
      <p>{{ formattedDate }}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: ["lastPeriodDate"], // מקבלת את תאריך הווסת האחרון מהמערכת
    computed: {
      formattedDate() {
        // אם יש תאריך שמור - נציג אותו, אחרת נשתמש בברירת המחדל
        return this.lastPeriodDate
          ? new Date(this.lastPeriodDate).toLocaleDateString("en-GB", {
              day: "2-digit",
              month: "2-digit",
              year: "numeric",
            })
          : "12/34/5678";
      },
    },
  };
  </script>
  
  <style scoped>
  .last-period-container {
    background: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 300px;
    margin: 20px auto;
  }
  h2 {
    color: #333;
  }
  p {
    font-size: 18px;
    font-weight: bold;
    color: #4CAF50;
  }
  </style>
  
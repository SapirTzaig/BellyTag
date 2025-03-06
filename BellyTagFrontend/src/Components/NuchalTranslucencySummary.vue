<template>
    <div class="nt-summary-card">
      <h3>Nuchal Translucency Screening</h3>
      <div class="nt-value" :class="riskLevelColor">
        NT: {{ ntValue }} mm
      </div>
      <p class="risk-level">Risk Level: <strong>{{ riskLevel }}</strong></p>
      <button @click="goToDetails">View Details</button>
    </div>
  </template>
  
  <script>
  import { defineComponent, computed } from "vue";
  import { useRouter } from "vue-router";
  
  export default defineComponent({
    setup() {
      const router = useRouter();
  
      // נתונים דיפולטיביים (אפשר למשוך ממסד נתונים)
      const ntValue = 1.9; // לדוגמה
  
      // חישוב רמת הסיכון לפי NT
      const riskLevel = computed(() => {
        if (ntValue < 2.5) return "Low";
        if (ntValue < 3.5) return "Medium";
        return "High";
      });
  
      // צבע רקע בהתאם לרמת הסיכון
      const riskLevelColor = computed(() => {
        return {
          low: ntValue < 2.5,
          medium: ntValue >= 2.5 && ntValue < 3.5,
          high: ntValue >= 3.5,
        };
      });
  
      // מעבר לעמוד הפירוט
      const goToDetails = () => {
        router.push("/nt-details");
      };
  
      return { ntValue, riskLevel, riskLevelColor, goToDetails };
    },
  });
  </script>
  
  <style scoped>
  .nt-summary-card {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .nt-value {
    font-size: 1.4rem;
    padding: 8px;
    border-radius: 5px;
  }
  
  .low {
    background-color: #c8e6c9;
    color: #2e7d32;
  }
  
  .medium {
    background-color: #fff3cd;
    color: #856404;
  }
  
  .high {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  button {
    margin-top: 10px;
    padding: 8px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  
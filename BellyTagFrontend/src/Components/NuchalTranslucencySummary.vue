<template>
  <div class="nt-summary-card">
    <h3>🩺 Nuchal Translucency</h3>
    <div class="nt-value" :class="riskLevelColor">
      NT: <span class="nt-number">{{ ntValue }}</span> mm
    </div>
    <p class="risk-level">
      Risk Level: <strong :class="riskLevelColor">{{ riskLevel }}</strong>
    </p>
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
      if (ntValue < 2.5) return "low";
      if (ntValue < 3.5) return "medium";
      return "high";
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
  background: linear-gradient(to bottom, #fdfbfb, #f8f9fa); /* רקע עם גרדיאנט */
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 280px;
  margin: 20px auto;
  transition: transform 0.3s ease-in-out;
}

.nt-summary-card:hover {
  transform: scale(1.05);
}

h3 {
  color: #333;
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
}

.nt-value {
  font-size: 1.4rem;
  padding: 10px;
  border-radius: 8px;
  font-weight: bold;
  display: inline-block;
  margin: 10px 0;
}

.nt-number {
  font-size: 1.8rem;
}

/* 🎨 צבעים לרמות סיכון */
.low {
  background-color: #e3fcef;
  color: #2e7d32;
  border: 1px solid #2e7d32;
}

.medium {
  background-color: #fff4e5;
  color: #b9770e;
  border: 1px solid #b9770e;
}

.high {
  background-color: #fde8e8;
  color: #c0392b;
  border: 1px solid #c0392b;
}

.risk-level strong {
  font-weight: bold;
  padding: 5px;
}

/* 🎨 כפתור מעוצב */
button {
  margin-top: 15px;
  padding: 10px 18px;
  background: #56a1f1;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
  box-shadow: 0 4px 6px rgba(0, 123, 255, 0.2);
}

button:hover {
  background: #0056b3;
  box-shadow: 0 6px 12px rgba(0, 123, 255, 0.3);
  transform: translateY(-2px);
}
</style>

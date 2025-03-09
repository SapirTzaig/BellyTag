<template>
  <div class="nasal-bone-card">
    <h3>👃 Nasal Bone Determination</h3>
    <p class="status-text">
      <strong>Status:</strong> <span :class="nasalBone ? 'normal' : 'danger'">
        {{ nasalBone ? "Present ✅" : "Absent ❌" }}
      </span>
    </p>
  </div>
</template>

<script>
export default {
  props: {
    nasalBone: {
      type: Boolean,
      required: true
    }
  }
};
</script>

<style scoped>
.nasal-bone-card {
  background: linear-gradient(to bottom, #fdfbfb, #f8f9fa);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 280px;
  margin: 20px auto;
  transition: transform 0.3s ease-in-out;
}

.nasal-bone-card:hover {
  transform: scale(1.05);
}

h3 {
  color: #333;
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
}

.status-text {
  font-size: 20px;
  font-weight: bold;
}

.normal {
  color: #2e7d32;
  background: #e3fcef;
  padding: 5px 12px;
  border-radius: 8px;
  display: inline-block;
}

.danger {
  color: #c0392b;
  background: #fde8e8;
  padding: 5px 12px;
  border-radius: 8px;
  display: inline-block;
}
</style>

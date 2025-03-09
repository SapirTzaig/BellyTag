<template>
    <div class="nasal-bone-card">
      <h3>Nasal Bone Determination</h3>
      <p><strong>Status:</strong> {{ nasalBone ? 'Present' : 'Absent' }}</p>
      <p :class="nasalBone ? 'normal' : 'danger'">
        {{ nasalBone ? "Nasal bone detected ✅" : "Nasal bone missing ❌" }}
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
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    min-height: 150px;
  }
  
  .normal {
    color: green;
    font-weight: bold;
  }
  
  .danger {
    color: red;
    font-weight: bold;
  }
  </style>
  
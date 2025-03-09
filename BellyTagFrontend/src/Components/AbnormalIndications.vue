<template>
    <div class="abnormal-indications-card">
      <h3>Possible Abnormal Indications</h3>
      <ul>
        <li v-for="(status, key) in indications" :key="key">
          <strong>{{ formatKey(key) }}:</strong> {{ status ? "Detected ❌" : "Normal ✅" }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      indications: Object
    },
    methods: {
      formatKey(key) {
        return key.replace(/_/g, " ");
      }
    }
  };
  </script>
  
  <style scoped>
  .abnormal-indications-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    min-height: 150px;
  }
  </style>
  
<template>
    <div class="upload">
      <h1>Upload Medical Document</h1>
      <input type="file" @change="handleFileUpload" />
      
      <!-- Display the extracted text from PDF -->
      <div v-if="extractedText">
        <h2>Extracted Text:</h2>
        <pre>{{ extractedText }}</pre>
      </div>
  
      <!-- Display the LLM analysis -->
      <div v-if="analysis">
        <h2>Analysis:</h2>
        <pre>{{ analysis }}</pre>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        extractedText: null,
        analysis: null,
      };
    },
    methods: {
      async handleFileUpload(event) {
        const file = event.target.files[0];
        const formData = new FormData();
        formData.append("file", file);
  
        const response = await fetch("http://localhost:5000/upload", {
          method: "POST",
          body: formData,
        });
  
        const result = await response.json();
        if (result.extracted_text) {
          this.extractedText = result.extracted_text;
          this.analysis = result.analysis;
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .upload {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  
  input[type="file"] {
    margin: 20px 0;
  }
  
  pre {
    background-color: #f4f4f4;
    padding: 10px;
    border-radius: 4px;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
  </style>
  
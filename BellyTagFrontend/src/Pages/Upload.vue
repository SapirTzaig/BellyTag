<template>
  <div class="upload">
    <h1>Upload Medical Document</h1>
    
    <!-- Dropdown to choose the test -->
    <div class="form-group">
      <label for="test-selection">Select Test:</label>
      <select v-model="selectedTest" id="test-selection">
        <option value="">Select Test</option>
        <option value="Ultrasound for Fetal Nuchal Translucency">Ultrasound for Fetal Nuchal Translucency</option>
        <option value="Ultrasound for Fetal Nasal Bone Determination">Ultrasound for Fetal Nasal Bone Determination</option>
        <option value="Maternal Serum (Blood) Tests">Maternal Serum (Blood) Tests</option>
        <option value="Genetic Screening Recommendation">Genetic Screening Recommendation</option>
        <option value="Multiple Marker Blood Tests (Second Trimester)">Multiple Marker Blood Tests (Second Trimester)</option>
        <option value="Possible Abnormal Indications">Possible Abnormal Indications</option>
        <option value="Follow-up Testing">Follow-up Testing</option>
        <option value="Screening Accuracy">Screening Accuracy</option>
        <option value="Group B Streptococcus Presence">Group B Streptococcus Presence</option>
      </select>
    </div>
    
    <!-- File upload input -->
    <input type="file" accept=".pdf" @change="handleFileUpload" />

    <!-- Display the extracted text from the uploaded file -->
    <div v-if="extractedText">
      <h2>Extracted Text:</h2>
      <pre>{{ extractedText }}</pre>
    </div>

    <!-- Display the LLM analysis -->
    <div v-if="analysis">
      <h2>Analysis:</h2>
      <pre>{{ analysis }}</pre>
    </div>

    <!-- List of previously uploaded files -->
    <div v-if="previousUploads.length > 0">
      <h2>Previous Uploads:</h2>
      <select v-model="selectedUpload">
        <option v-for="(file, index) in previousUploads" :key="index" :value="file">
          {{ file.name }} - {{ file.date }}
        </option>
      </select>
      <!-- Checkbox for sending files via email -->
      <div v-for="(file, index) in previousUploads" :key="index" class="checkbox-container">
        <input type="checkbox" v-model="file.selected" /> 
        <label>{{ file.name }}</label>
      </div>
    </div>

    <button @click="sendFilesByEmail" :disabled="!selectedFiles.length">Send Files to Email</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedTest: "",
      selectedUpload: null,
      extractedText: null,
      analysis: null,
      previousUploads: [],
    };
  },
  computed: {
    selectedFiles() {
      return this.previousUploads.filter(file => file.selected);
    },
  },
  methods: {
    async handleFileUpload(event) {
      const file = event.target.files[0];
      
      if (file && file.type === "application/pdf") {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("testType", this.selectedTest);

        try {
          const response = await fetch("http://localhost:5000/upload", {
            method: "POST",
            body: formData,
          });

          const result = await response.json();

          if (result.extracted_text) {
            this.extractedText = result.extracted_text;
            this.analysis = result.analysis;

            // Save the file locally (mock for desktop)
            const filePath = r`C:\Users\sapir\OneDrive\Desktop\saved${file.name}`;  // Update this path as needed
            this.previousUploads.push({
              name: file.name,
              date: new Date().toLocaleString(),
              path: filePath,
              selected: false,
            });
          }
        } catch (error) {
          alert("Error uploading the file.");
        }
      } else {
        alert("Please upload a valid PDF file.");
      }
    },

    async sendFilesByEmail() {
      const filesToSend = this.selectedFiles.map(file => ({
        name: file.name,
        path: file.path,
      }));

      try {
        const response = await fetch("http://localhost:5000/send-email", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ files: filesToSend }),
        });

        const result = await response.json();

        if (response.ok) {
          alert("Files sent successfully!");
        } else {
          alert("Error sending files. Please try again.");
        }
      } catch (error) {
        alert("An error occurred while sending files.");
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

select {
  width: 100%;
  padding: 8px;
  margin: 10px 0;
  border-radius: 4px;
}

.checkbox-container {
  margin-top: 10px;
}

pre {
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-wrap: break-word;
}

button {
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover {
  background-color: #45a049;
}
</style>

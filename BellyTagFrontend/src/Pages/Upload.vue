<template>
  <div class="upload">
    <h1>Upload Medical Document</h1>

    <!-- Dropdown to choose the test -->
    <div class="form-group">
      <label for="test-selection">Select Test:</label>
      <select v-model="selectedTest" id="test-selection">
        <!-- Dropdown options for tests -->
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
    <input type="file" accept=".png,.pdf" @change="handleFileUpload" />

    <!-- Toast Notification -->
    <div v-if="toastMessage" class="toast" :class="toastType">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      barcode: "",
      selectedTest: "",
      toastMessage: "",
      toastType: "",
    };
  },
  mounted() {
    this.barcode = this.$route.params.barcode; // Get barcode from URL
  },
  methods: {
    async handleFileUpload(event) {
      const file = event.target.files[0];

      if (!file) {
        this.showToast("Please select a file to upload.", "error");
        return;
      }

      if (!this.selectedTest) {
        this.showToast("Please select a test type before uploading.", "error");
        return;
      }

      // Generate timestamp and new file name
      const timestamp = new Date().toISOString().replace(/[-T:.Z]/g, ""); // Format timestamp
      const newFileName = `${this.selectedTest}_${timestamp}${file.name.slice(file.name.lastIndexOf('.'))}`; // Use file extension

      // Create FormData
      const formData = new FormData();
      formData.append("newFileName", newFileName); // Append new file name
      formData.append("barcode", this.barcode); // Append barcode from URL

      try {
        const response = await fetch("http://localhost:5000/upload/${this.barcode}", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          this.showToast("File uploaded successfully!", "success");
        } else {
          throw new Error("Something went wrong. Please try again.");
        }
      } catch (error) {
        this.showToast(error.message, "error");
      }
    },

    showToast(message, type) {
      this.toastMessage = message;
      this.toastType = type;

      setTimeout(() => {
        this.toastMessage = "";
      }, 3000);
    },
  },
};
</script>

<style scoped>
.upload {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  font-size: 24px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}

select,
input[type="file"] {
  width: 100%;
  padding: 10px;
  margin-top: 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 16px;
}

select:focus,
input[type="file"]:focus {
  border-color: #4caf50;
  outline: none;
}

button {
  display: block;
  width: 100%;
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover {
  background-color: #45a049;
}

.checkbox-container {
  margin-top: 10px;
}

.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px;
  color: white;
  border-radius: 8px;
  text-align: center;
  width: 300px;
  font-size: 16px;
  font-weight: 500;
}

.toast.success {
  background-color: #4caf50;
}

.toast.error {
  background-color: #e74c3c;
}

pre {
  background-color: #f4f4f4;
  padding: 12px;
  border-radius: 6px;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 14px;
}
</style>

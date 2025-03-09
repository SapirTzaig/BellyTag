<template>
    <div class="generate-barcode">
      <h1>Generate Temporary Barcode for Doctor</h1>
      <p>This barcode will be valid for 5 minutes only. Click "Generate" to create a temporary barcode for your doctor.</p>
      
      <button @click="generateTemporaryBarcode">Generate</button>
  
      <div v-if="temporaryBarcode">
        <p><strong>Temporary Barcode:</strong> {{ temporaryBarcode }}</p>
        
        <!-- Display the QR code -->
        <div v-if="qrCodeUrl">
          <img :src="qrCodeUrl" alt="QR Code" />
        </div>
  
        <button @click="downloadBarcode">Download Barcode</button>
      </div>
  
      <p v-if="message" :class="messageType">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import QRCode from 'qrcode'; // Import the QR code library
  
  export default {
    props: ['barcode'], // Accept barcode as a prop from the URL
  
    data() {
      return {
        temporaryBarcode: '',
        email: '',
        message: '',
        messageType: '', // "success" or "error"
        qrCodeUrl: '', // Store QR code image URL
      };
    },
  
    methods: {
      generateTemporaryBarcode() {
        // Use the barcode from the URL directly (no new barcode is generated)
        const barcode = sessionStorage.getItem('barcode') || this.barcode;
  
        // Generate expiry timestamp (5 minutes from now)
        this.temporaryBarcode = `${barcode}`; // Append expiry to the barcode
  
        // Generate the QR code from the barcode
        this.generateQRCode(this.temporaryBarcode);
  
        this.message = "Temporary barcode generated!";
        this.messageType = "success";
      },
  
      generateQRCode(data) {
        QRCode.toDataURL(data) // Generate the QR code as a Data URL
          .then(url => {
            this.qrCodeUrl = url; // Set the QR code URL for the image
          })
          .catch(err => {
            console.error("Error generating QR code:", err);
          });
      },
  
      downloadBarcode() {
        if (this.temporaryBarcode) {
          const blob = new Blob([this.temporaryBarcode], { type: 'text/plain' });
          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);
          link.download = `${this.temporaryBarcode}.txt`;
          link.click();
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .generate-barcode {
    max-width: 600px;
    margin: 50px auto;
    padding: 30px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #ffffff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  button {
    display: inline-block;
    padding: 10px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  input[type="email"] {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  input[type="email"]:focus {
    border-color: #4caf50;
    outline: none;
  }
  
  .message.success {
    color: #4caf50;
  }
  
  .message.error {
    color: #e74c3c;
  }
  
  p {
    font-size: 16px;
    color: #333;
  }
  
  h1 {
    font-size: 24px;
    text-align: center;
    color: #333;
  }
  </style>
  
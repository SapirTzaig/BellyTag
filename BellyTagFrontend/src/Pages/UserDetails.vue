<template>
  <div class="user-card">
    <!-- Profile Section: Avatar and Name -->
    <div class="profile-section">
      <img :src="user.avatar || defaultAvatar" alt="User Avatar" class="avatar" />
      <h2>{{ user.name }}</h2>
      <p class="role">{{ user.status }}</p>

      <!-- Barcode Image -->
      <img :src="barcodeImage" alt="Barcode" class="barcode" />
      
    </div>

    <!-- User Info Section -->
    <div class="info-section">
      <h3>User Details</h3>
      <div class="info">
        <p><strong>Name:</strong> {{ user.Name }}</p>
        <p><strong>Age:</strong> {{ user.Age }}</p>
        <p><strong>Date of Birth:</strong> {{ user.DoB }}</p>
        <p><strong>Gender:</strong> {{ user.Gender }}</p>
        <p><strong>Status:</strong> {{ user.Status }}</p>
        <p><strong>Email:</strong> {{ user.Email }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import defaultAvatar from '@/Assets/woman.png'; // Default avatar image
import barcodeImage from '@/Assets/barcode.png'; // Barcode image

export default {
  data() {
    return {
      user: {
        Name: '',
        Age: '',
        DoB: '',
        Gender: '',
        Status: '',
        Email: '',
        barcode: sessionStorage.getItem('barcode') || '', // Barcode from sessionStorage
      },
      defaultAvatar, // Default user avatar
      barcodeImage,  // Barcode image
    };
  },
  async created() {
    // Retrieve the barcode from sessionStorage
    const barcode = sessionStorage.getItem('barcode');
    
    // If barcode is not found (user is not logged in), redirect to login page
    if (!barcode) {
      this.$router.push('/'); // Redirect to login page
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/personal?barcode=${barcode}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });


      // Parse the response data
      const data = await response.json();
      console.log(data);


      if (response.ok) {
        // Populate user details with the data received
        this.user.Name = data.Name;
        this.user.Age = data.Age;
        this.user.DoB = data.DoB;
        this.user.Gender = data.Gender;
        this.user.Status = data.Status;
        this.user.Email = data.Email;
      } else {
        console.error("Error fetching user details:", data.message);
      }
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  }
};
</script>

<style scoped>
.user-card {
  display: flex;
  max-width: 800px;
  margin: 20px auto;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  font-family: Arial, sans-serif;
}

/* Profile Section */
.profile-section {
  background: linear-gradient(135deg, #ff7e5f, #feb47b);
  color: white;
  padding: 30px;
  text-align: center;
  width: 40%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.avatar {
  width: 170px;
  height: 170px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.barcode {
  width: 120px;
}

.role {
  font-size: 18px;
  opacity: 0.9;
}

/* Info Section */
.info-section {
  padding: 30px;
  width: 60%;
}

h3 {
  font-size: 22px;
  margin-bottom: 15px;
  color: #2c3e50;
  border-bottom: 1px solid #ddd;
  padding-bottom: 5px;
}

.info {
  margin-bottom: 20px;
}

p {
  font-size: 18px;
  margin: 8px 0;
}

/* Social Links */
.social-links {
  margin-top: 20px;
  text-align: center;
}

.social-links a {
  margin: 0 10px;
  font-size: 24px;
  color: #2c3e50;
  text-decoration: none;
}

.social-links a:hover {
  color: #ff7e5f;
}

/* Font Awesome Icons */
.fab {
  font-family: "Font Awesome 5 Free";
}
</style>

<template>
    <div class="user-card">
      <!-- צד שמאל: תמונת פרופיל ושם -->
      <div class="profile-section">
        <img :src="user.avatar || defaultAvatar" alt="User Avatar" class="avatar" />
        <h2>{{ user.name }}</h2>
        <p class="role">{{ user.status }}</p>
  
        <!-- ✅ תמונת הברקוד מתחת לתמונה -->
        <img :src="barcodeImage" alt="Barcode" class="barcode" />
      </div>
  
      <!-- צד ימין: פרטי המשתמש לפי הסדר המבוקש -->
      <div class="info-section">
        <h3>User Details</h3>
        <div class="info">
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Age:</strong> {{ user.age }}</p>
          <p><strong>Date of Birth:</strong> {{ user.date_of_birth }}</p>
          <p><strong>Gender:</strong> {{ user.gender }}</p>
          <p><strong>Status:</strong> {{ user.status }}</p>
  
          <!-- ✅ הצגת מספר הילדים רק אם יש -->
          <p v-if="user.children_count !== undefined && user.children_count > 0">
            <strong>Children:</strong> {{ user.children_count }}
          </p>
  
          <p><strong>Phone:</strong> {{ user.phone || 'N/A' }}</p>
          <p><strong>Email:</strong> {{ user.mail }}</p>
        </div>
  
        <!-- רשתות חברתיות -->
        <div class="social-links">
          <a href="#" target="_blank"><i class="fab fa-facebook"></i></a>
          <a href="#" target="_blank"><i class="fab fa-twitter"></i></a>
          <a href="#" target="_blank"><i class="fab fa-instagram"></i></a>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import defaultAvatar from '@/Assets/woman.png'; // ✅ ייבוא תמונת הפרופיל הדיפולטיבית
  import barcodeImage from '@/Assets/barcode.png'; // ✅ ייבוא תמונת הברקוד
  
  export default {
    data() {
      return {
        user: {
          avatar: '',
          children_count: 0
        },
        defaultAvatar, // תמונה דיפולטיבית של המשתמש
        barcodeImage // תמונת הברקוד
      };
    },
    async created() {
      try {
        const response = await fetch('http://localhost:5000/user'); // עדכן את ה-API שלך
        const data = await response.json();
        this.user = data;
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
  
  /* צד שמאל - מידע משתמש */
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
  
  /* צד ימין - פרטים */
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
  
  /* רשתות חברתיות */
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
  
  /* אייקונים (Font Awesome) */
  .fab {
    font-family: "Font Awesome 5 Free";
  }
  </style>
  
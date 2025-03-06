import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import RegisterPage from './Pages/RegisterPage.vue';
import Login from './Pages/Login.vue';
import Upload from './Pages/Upload.vue';
import Dashboard from './Pages/Dashboard.vue';
import PatientScreen from './Pages/PatientScreen.vue';
import UserDetails from './Pages/UserDetails.vue';
import NuchalTranslucencyDetails from './Pages/NuchalTranslucencyDetails.vue';


const routes = [
  { path: '/register', component: RegisterPage },
  { path: '/', component: Login },
  { path: '/upload/:barcode', component: Upload },
  { path: '/dashboard', component: Dashboard },
  { path: '/patient/:barcode', component: PatientScreen },
  { path: '/user-details', component: UserDetails },
  { path: '/nt-details', component: NuchalTranslucencyDetails },

  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount('#app');

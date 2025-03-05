import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import Login from './Pages/Login.vue';
import Upload from './Pages/Upload.vue';
import Dashboard from './Pages/Dashboard.vue';
import PatientScreen from './Pages/PatientScreen.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/upload', component: Upload },
  { path: '/dashboard', component: Dashboard },
  { path: '/patient/:id', component: PatientScreen }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount('#app');

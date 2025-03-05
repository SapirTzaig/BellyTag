import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import Login from './components/Login.vue';
import Upload from './components/Upload.vue';
import Dashboard from './components/Dashboard.vue';
import PatientScreen from './components/PatientScreen.vue';

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

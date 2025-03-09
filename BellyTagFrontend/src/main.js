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
import DoctorPatientScreen from './Pages/DoctorPatientScreen.vue';
import BloodTests from '@/Components/BloodTests.vue';
import BloodTestsHistory from '@/Pages/BloodTestsHistory.vue';
import GenerateBarcode from '@/Pages/GenerateBarcode.vue';

const routes = [
  { path: '/register', name: 'register', component: RegisterPage },
  { path: '/', name: 'login', component: Login },
  { path: '/upload/:barcode', component: Upload },
  { path: '/dashboard', component: Dashboard },
  { path: '/patient/:barcode', component: PatientScreen },
  { path: '/Doctor_patient/:barcode', component: DoctorPatientScreen },
  { path: '/user-details', component: UserDetails },
  { path: '/nt-details', component: NuchalTranslucencyDetails },
  { path: '/blood-tests-history', component: BloodTestsHistory },
  { path: '/generate/:barcode', component: GenerateBarcode },
];

document.title = "DocHumation";

const link = document.createElement("link");
link.rel = "icon";
link.type = "image/x-icon";
link.href = "src/Assets/docho.ico"; // Path relative to the public folder
document.head.appendChild(link);

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount('#app');

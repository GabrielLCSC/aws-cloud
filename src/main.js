import { Amplify } from 'aws-amplify';
import amplifyconfig from './amplifyconfiguration.json';
import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/main.css'
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Antd from 'ant-design-vue'

Amplify.configure(amplifyconfig);

const app = createApp(App)

app.use(router)
app.use(Antd)
c
app.mount('#app')

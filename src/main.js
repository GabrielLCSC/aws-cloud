import './amplifyConfig'
import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/main.css'
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Antd from 'ant-design-vue'
import { Amplify } from '@aws-amplify/core'
import amplifyconfig from './amplifyconfiguration.json'

Amplify.configure(amplifyconfig)

const app = createApp(App)

app.use(router)
app.use(Antd)

app.mount('#app')

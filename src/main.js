import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

let app = createApp(App)

app.use(router).mount('#app')
app.use(Toast, {
    timeout: 3000
});
app.use(require('vue-cookies'))

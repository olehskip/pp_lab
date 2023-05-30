import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import VueCookies from 'vue-cookies'
let app = createApp(App)

app.use(Toast, {
    timeout: 3000
});
app.use(VueCookies, { expires: '7d'})
app.use(router).mount('#app')

import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import auth from './store/authentication.js'

const app = createApp(App)
app.use(router)

// Make auth state available globally as $auth
app.config.globalProperties.$auth = auth

app.mount('#app')

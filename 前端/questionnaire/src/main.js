import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";

import ElementPlus from 'element-plus';
import 'element-plus/lib/theme-chalk/index.css';
import print from 'print-js'

createApp(App)
    .use(ElementPlus)
    .use(store)
    .use(router)
    .mount("#app");
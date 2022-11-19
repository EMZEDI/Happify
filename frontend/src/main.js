import { createApp } from 'vue'
import {createRouter, createWebHistory} from 'vue-router'
import App from './App.vue'

import './assets/main.css'
import './assets/blobz.min.css'

import PlayerPage from './components/PlayerPage.vue'
import PlaylistSetup from './components/PlaylistSetup.vue'


const routes = [
    { path: '/', component: PlaylistSetup },
    { path: '/dashboard', component: PlayerPage },
]
const router = createRouter({
    history: createWebHistory(),
    routes
})


createApp(App).use(router).mount('#app')

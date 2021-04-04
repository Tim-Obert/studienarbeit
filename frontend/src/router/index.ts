import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Overview from "@/views/Overview.vue";
import SingleStream from "@/views/SingleStream.vue";
import Settings from "@/views/Settings.vue";
import Recordings from "@/views/Recordings.vue";

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Overview',
    component: Overview
  },
  {
    path: '/recorded',
    name: 'Recordings',
    component: Recordings
  },
  {
    path: '/stream/:id',
    name: 'SingleStream',
    component: SingleStream
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

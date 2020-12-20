import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Home from '../views/Home.vue'
import Overview from "@/views/Overview.vue";
import Recorded from "@/views/Recorded.vue";
import SingleStream from "@/views/SingleStream.vue";
import Settings from "@/views/Settings.vue";

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/overview',
    name: 'Overview',
    component: Overview
  },
  {
    path: '/recorded',
    name: 'Recorded',
    component: Recorded
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

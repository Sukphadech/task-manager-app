<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>

    <div>

      <nav>
        <router-link to="/login">Login</router-link> |
        <router-link to="/dashboard">Dashboard</router-link> |
        <router-link to="/board/1">Board 1</router-link>
      </nav>
      <router-view />
    </div>
  </header>

  <RouterView />
</template>

<style >

</style>

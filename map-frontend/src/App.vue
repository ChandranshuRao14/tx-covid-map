<template>
  <div id="app">
    <Navbar />
    <Map />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import Map from './components/Map.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Map
  },

}
</script>

<style>
  html, body {
      font-family: 'Open Sans', sans-serif !important;
      margin: 0;
      padding: 0;
      background-color: #fafbfe !important;
  }
</style>

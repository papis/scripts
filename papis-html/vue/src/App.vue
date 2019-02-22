<template>
  <div id="app">
    <List/>
  </div>
</template>

<script>
import Vue from 'vue'
import VueMaterial from 'vue-material'
import List from './components/List.vue'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default-dark.css'

Vue.use(VueMaterial)

export default {
  name: 'app',
  components: {
    List
  }
}
</script>

<style>
</style>

<template>
  <v-app>
    <SideBar v-if="showSidebar" />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import SideBar from './components/SideBar.vue'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'App',
  components: {
    SideBar,
  },
  setup() {
    const route = useRoute()
    
    const showSidebar = computed(() => route.path !== '/login')

    return {
      showSidebar
    }
  }
}
</script>

<style>
@import '~vuetify/styles';
@import '~@mdi/font/css/materialdesignicons.css';
</style>

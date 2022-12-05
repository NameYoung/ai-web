<template>
  <v-app>
    <v-app-bar flat color="light-blue lighten-5" app>
      <v-app-bar-title>AI Web</v-app-bar-title>
    </v-app-bar>
    <SideMenu/>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>

</template>


<script>
import SideMenu from '@/components/SideMenu.vue'
export default {
  name: 'App',

  components: {
    SideMenu
  }
};
</script>

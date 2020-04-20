<template>
  <v-app id="background">
    <toolbar />
    <v-fade-transition mode="out-in">
      <router-view></router-view>
    </v-fade-transition>
  </v-app>
</template>

<script>
import toolbar from "./components/toolbar";

export default {
  name: "App",

  components: {
    toolbar
  },

  data: () => ({
    //
  })
};
</script>

<style>
#background {
  background-color:#444444
}
</style>

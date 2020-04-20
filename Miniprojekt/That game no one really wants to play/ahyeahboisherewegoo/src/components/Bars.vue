<template>
  <v-container fluid>
    <v-row justify="space-around" no-gutters>
      <v-col cols="4">
        <v-slider color="red" v-model="this.$store.state.health"></v-slider>
      </v-col>
      <v-col cols="4">
        <v-slider color="green" v-model="this.$store.state.popularity"></v-slider>
      </v-col>
      <v-col cols="4">
        <v-slider v-model="this.$store.state.influence"></v-slider>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Bars",

  computed: {
    ...mapGetters(["health", "popularity", "influence"])
  }
};
</script>

<style>
</style>
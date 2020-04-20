<template>
  <div>
    <v-app-bar color="orange" dark>
      <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
      <v-toolbar-title>I don't really know what to put here. It's a navbar so...</v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" absolute temporary color="white">
      <v-list nav dense shaped>
        <v-list-item-group v-model="group" active-class="orange--text text--accent-4">
          <v-list-item href="/">
            <v-list-item-icon>
              <v-icon>mdi-home</v-icon>
            </v-list-item-icon>
            <v-list-item-title>"Home" or "Startpage"</v-list-item-title>
          </v-list-item>

          <v-list-item href="/play">
            <v-list-item-icon>
              <v-icon>mdi-album</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Play the actual game</v-list-item-title>
          </v-list-item>
          <v-spacer></v-spacer>
          <v-list-item href="/about">
            <v-list-item-icon>
              <v-icon>mdi-spin mdi-help</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Wut</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  data: () => ({
    drawer: false
  })
};
</script>
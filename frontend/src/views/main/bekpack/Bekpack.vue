<template>
  <div>
    <div v-if="hasAccount">
      <v-toolbar light>
        <v-toolbar-title> Your BekPack</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          :to="{
            name: 'bekpack-create-trip',
          }"
          >Create Trip</v-btn
        >
      </v-toolbar>
    </div>
    <div v-if="!hasAccount">
      <p>It looks like you haven't yet activated BekPack</p>
      <p>
        <v-btn @click="registerAccount"> Activate! </v-btn>
      </p>
      <v-toolbar light>
        <v-toolbar-title> Bekpack not yet activated</v-toolbar-title>
        <v-spacer></v-spacer>
        <div>It looks like you haven't yet activated BekPack</div>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="registerAccount"> Activate!</v-btn>
      </v-toolbar>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import {
  dispatchCreateBekpackUser,
  dispatchGetBekpackUser,
  dispatchGetMyTrips,
} from "@/store/bekpack/actions";
import {
  readTrips,
  readUser,
  readUserHasAccount,
} from "@/store/bekpack/getters";
@Component
export default class Bekpack extends Vue {
  public async mounted() {
    this.load();
  }
  public async load() {
    await dispatchGetBekpackUser(this.$store);
    await dispatchGetMyTrips(this.$store);
  }
  public async registerAccount() {
    await dispatchCreateBekpackUser(this.$store);
    await this.load();
  }
  get user() {
    return readUser(this.$store);
  }
  get hasAccount() {
    return readUserHasAccount(this.$store);
  }
  get trips() {
    return readTrips(this.$store);
  }
}
</script>

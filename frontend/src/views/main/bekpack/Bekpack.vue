<template>
  <div>
    <h1>Welcome to BekPack!</h1>
    <div v-if="hasAccount">You are logged in! Time for no more anxiety!</div>
    <div v-if="!hasAccount">
      <p>It looks like you haven't yet activated BekPack</p>
      <p>
        <v-btn @click="registerAccount"> Activate! </v-btn>
      </p>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { dispatchDeleteItem, dispatchGetItems } from "@/store/item/actions";
import { readItems, readItemsOneUser } from "@/store/item/getters";
import { readUserProfile } from "@/store/main/getters";
import { IItem } from "@/interfaces";
import {
  dispatchCreateBekpackUser,
  dispatchGetBekpackUser,
} from "@/store/bekpack/actions";
import { readUser, readUserHasAccount } from "@/store/bekpack/getters";
@Component
export default class Bekpack extends Vue {
  public async mounted() {
    await dispatchGetBekpackUser(this.$store);
  }
  get user() {
    return readUser(this.$store);
  }
  get hasAccount() {
    return readUserHasAccount(this.$store);
  }
  public async registerAccount() {
    await dispatchCreateBekpackUser(this.$store);
  }
}
</script>

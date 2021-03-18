<template>
  <router-view></router-view>
</template>

<script lang="ts">
import { store } from "@/store";
import { readHasAdminAccess } from "@/store/main/getters";
import { Component, Vue } from "vue-property-decorator";

const routeGuardAdmin = async (to, from, next) => {
  if (!readHasAdminAccess(store)) {
    next("/main");
  } else {
    next();
  }
};

@Component
export default class Admin extends Vue {
  public beforeRouteEnter(to, from, next) {
    routeGuardAdmin(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardAdmin(to, from, next);
  }
}
</script>

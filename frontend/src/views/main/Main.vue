<template>
  <div>
    <v-navigation-drawer
      persistent
      :mini-variant="miniDrawer"
      v-model="showDrawer"
      fixed
      app
    >
      <v-layout column fill-height>
        <v-list>
          <v-subheader>Main menu</v-subheader>
          <v-list-item :to="{ name: 'bekpack-home' }">
            <v-list-item-action>
              <v-icon>flight</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Bekpack</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/items">
            <v-list-item-action>
              <v-icon>web</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Your Items</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/dashboard">
            <v-list-item-action>
              <v-icon>web</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Dashboard</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/chatSocket">
            <v-list-item-action>
              <v-icon>web</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>chatSocket</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/profile/view">
            <v-list-item-action>
              <v-icon>person</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Profile</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/profile/edit">
            <v-list-item-action>
              <v-icon>edit</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Edit Profile</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/profile/password">
            <v-list-item-action>
              <v-icon>vpn_key</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Change Password</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-divider></v-divider>
        <v-list subheader v-show="hasAdminAccess">
          <v-subheader>Admin</v-subheader>
          <v-list-item to="/main/admin/users/all">
            <v-list-item-action>
              <v-icon>group</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Manage Users</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/admin/users/create">
            <v-list-item-action>
              <v-icon>person_add</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Create User</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-spacer></v-spacer>
        <v-list>
          <v-list-item @click="logout">
            <v-list-item-action>
              <v-icon>close</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="switchMiniDrawer">
            <v-list-item-action>
              <v-icon
                v-html="miniDrawer ? 'chevron_right' : 'chevron_left'"
              ></v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Collapse</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-layout>
    </v-navigation-drawer>
    <!-- TODO: fix v-app-bar rendering too far to the left -->

    <v-main>
      <v-app-bar dark color="primary">
        <v-icon @click.stop="switchShowDrawer">mdi-hamburger</v-icon>
        <v-spacer></v-spacer>

        <v-app-bar-title v-text="appName"></v-app-bar-title>
        <v-spacer></v-spacer>
        <v-menu>
          <template v-slot:activator="{ on }">
            <v-btn v-on="on" icon>
              <v-icon>more_vert</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item to="/main/profile">
              <v-list-item-content>
                <v-list-item-title>Profile</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon>person</v-icon>
              </v-list-item-action>
            </v-list-item>
            <v-list-item @click="logout">
              <v-list-item-content>
                <v-list-item-title>Logout</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon>close</v-icon>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-app-bar>
      <router-view></router-view>
    </v-main>
    <v-footer class="pa-0" fixed>
      <v-spacer></v-spacer>
      <span>&copy; {{ appName }}</span>
    </v-footer>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import { appName } from "@/env";
import { dispatchUserLogOut } from "@/store/main/actions";
import {
  readDashboardMiniDrawer,
  readDashboardShowDrawer,
  readHasAdminAccess,
} from "@/store/main/getters";
import {
  commitSetDashboardMiniDrawer,
  commitSetDashboardShowDrawer,
} from "@/store/main/mutations";

const routeGuardMain = async (to, from, next) => {
  if (to.path === "/main") {
    next("/main/dashboard");
  } else {
    next();
  }
};

@Component
export default class Main extends Vue {
  public appName = appName;

  public beforeRouteEnter(to, from, next) {
    routeGuardMain(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    routeGuardMain(to, from, next);
  }

  get miniDrawer() {
    return readDashboardMiniDrawer(this.$store);
  }

  get showDrawer() {
    return readDashboardShowDrawer(this.$store);
  }

  set showDrawer(value) {
    commitSetDashboardShowDrawer(this.$store, value);
  }

  public switchShowDrawer() {
    commitSetDashboardShowDrawer(
      this.$store,
      !readDashboardShowDrawer(this.$store)
    );
  }

  public switchMiniDrawer() {
    commitSetDashboardMiniDrawer(
      this.$store,
      !readDashboardMiniDrawer(this.$store)
    );
  }

  public get hasAdminAccess() {
    return readHasAdminAccess(this.$store);
  }

  public async logout() {
    await dispatchUserLogOut(this.$store);
  }
}
</script>

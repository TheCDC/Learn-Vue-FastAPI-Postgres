<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title> Manage Users </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/users/create">Create User</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="users">
      <template v-slot:[`item.id`]="{ item }">
        <v-tooltip top>
          <span>Edit </span>
          <template v-slot:activator="{ on }">
            <v-btn
              text
              v-on="on"
              :to="{
                name: 'main-admin-users-edit',
                params: { id: item.id },
              }"
              ><v-icon>edit</v-icon>
            </v-btn>
          </template>
        </v-tooltip>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { IUserProfile } from "@/interfaces";
import { dispatchGetUsers } from "@/store/admin/actions";
import { readAdminUsers } from "@/store/admin/getters";
import { Component, Vue } from "vue-property-decorator";
import { Store } from "vuex";

@Component
export default class AdminUsers extends Vue {
  public headers = [
    {
      text: "Name",
      sortable: true,
      value: "name",
      align: "left",
    },
    {
      text: "Email",
      sortable: true,
      value: "email",
      align: "left",
    },
    {
      text: "Full Name",
      sortable: true,
      value: "full_name",
      align: "left",
    },
    {
      text: "Is Active",
      sortable: true,
      value: "isActive",
      align: "left",
    },
    {
      text: "Is Superuser",
      sortable: true,
      value: "isSuperuser",
      align: "left",
    },
    {
      text: "Actions",
      value: "id",
    },
  ];
  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }
}
</script>

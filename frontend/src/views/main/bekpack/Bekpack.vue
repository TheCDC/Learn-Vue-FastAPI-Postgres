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

    <div>
      <v-data-table
        :headers="headers"
        :items="trips"
        :footer-props="{
          showFirstLastPage: true,
        }"
      >
        <template v-slot:[`item.name`]="{ item }">
          <v-chip class="ma-2" :color="item.color">
            {{ item.name | truncate(100, "...") }}
          </v-chip>
        </template>
        <template v-slot:[`item.description`]="{ item }">
          {{ item.description | truncate(100, "...") }}
        </template>

        <template v-slot:[`item.id`]="{ item }">
          <v-spacer> </v-spacer>
          <v-tooltip top>
            <span>Edit </span>
            <template v-slot:activator="{ on }">
              <v-btn
                text
                v-on="on"
                :to="{
                  name: 'bekpack-edit-trip',
                  params: { id: item.id },
                }"
                ><v-icon>edit</v-icon>
              </v-btn>
            </template>
          </v-tooltip>
          <v-tooltip top>
            <span>Delete </span>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on" text @click="deleteTrip(item)"
                ><v-icon>delete</v-icon>
              </v-btn>
            </template>
          </v-tooltip>
        </template>
      </v-data-table>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import {
  dispatchCreateBekpackUser,
  dispatchDeleteTrip,
  dispatchGetBekpackUser,
  dispatchGetMyTrips,
} from "@/store/bekpack/actions";
import {
  readTrips,
  readUser,
  readUserHasAccount,
} from "@/store/bekpack/getters";
import { IBekpackTrip } from "@/interfaces";
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
  public async deleteTrip(t: IBekpackTrip) {
    await dispatchDeleteTrip(this.$store, t);
  }
  public headers = [
    { text: "name", sortable: true, value: "name", align: "left" },
    {
      text: "description",
      sortable: true,
      value: "description",
      align: "left",
    },
    { text: "Actions", sortable: false, value: "id" },
  ];
}
</script>

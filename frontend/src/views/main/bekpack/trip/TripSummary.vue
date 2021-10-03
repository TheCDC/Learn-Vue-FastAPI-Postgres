<template>
  <div>
    <v-progress-circular :indeterminate="true" v-if="!trip">
    </v-progress-circular>
    <v-card :color="trip.color" v-if="trip">
      <v-card-title>
        {{ trip.name }}
      </v-card-title>
      <v-card-subtitle>
        Created: {{ trip.time_created | localeDate }}

        Last modified : {{ trip.time_updated | localeDate }}
      </v-card-subtitle>
      <v-card-text>
        {{ trip.description }}
      </v-card-text>
      <v-card-actions>
        <v-btn
          :to="{
            name: 'bekpack-edit-trip',
            params: { tripId: trip.id },
          }"
        >
          edit
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-toolbar dark color="gray">
      Lists

      <v-btn
        :to="{
          name: 'bekpack-create-itemlist',
          params: { tripId: trip.id },
        }"
      >
        +
      </v-btn>
    </v-toolbar>
    <div class="d-flex flex-row justify-start flex-wrap">
      <v-card v-for="itemlist in itemlistsPage.items" :key="itemlist.id">
        <v-card-text>
          <v-toolbar :color="itemlist.color">
            {{ itemlist.name }}
          </v-toolbar>
          <v-card-actions>
            <v-btn
              :to="{
                name: 'bekpack-edit-itemlist',
                params: { itemlistId: itemlist.id },
              }"
            >
              EDIT
            </v-btn>
            <v-spacer />
            <v-btn @click="deleteChild(itemlist)"> DELETE </v-btn>
          </v-card-actions>
          <v-data-table
            :items="itemlist.items"
            :headers="[
              { text: 'Name', value: 'name' },
              { text: 'Quantity', value: 'quantity' },
            ]"
            :disable-pagination="true"
            :hide-default-footer="true"
          >
          </v-data-table>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>
<script lang="ts">
import { IBekpackItemList } from "@/interfaces/bekpack.ts/bekpackitemlist";
import { IBekpackItemListItem } from "@/interfaces/bekpack.ts/bekpackitemlistitem";
import { IPageRead } from "@/interfaces/common";
import { dispatchGetTrip } from "@/store/bekpack/actions";
import { readTripsOne } from "@/store/bekpack/getters";
import {
  dispatchDeleteBekpackItemlist,
  dispatchGetBekpackItemlistMulti,
} from "@/store/bekpack/itemlist/actions";
import { readItemlistPage } from "@/store/bekpack/itemlist/getters";
import { Component, Vue, Watch } from "vue-property-decorator";
@Component
export default class Bekpack extends Vue {
  public pageCursor: IPageRead = { page: 0, size: 64 };
  public mounted() {
    dispatchGetTrip(this.$store, { id: this.tripId });
    dispatchGetBekpackItemlistMulti(this.$store, {
      tripId: this.tripId,
      page: this.pageCursor,
    });
  }
  public get itemlistsPage() {
    return readItemlistPage(this.$store);
  }
  public get tripId() {
    return +this.$router.currentRoute.params.tripId;
  }
  public get trip() {
    return readTripsOne(this.$store)(this.tripId);
  }

  public async deleteChild(item: IBekpackItemList) {
    await dispatchDeleteBekpackItemlist(this.$store, item);
    dispatchGetBekpackItemlistMulti(this.$store, {
      tripId: this.tripId,
      page: this.pageCursor,
    });
  }
}
</script>

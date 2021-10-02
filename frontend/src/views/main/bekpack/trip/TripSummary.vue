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
    <v-toolbar dense color="gray">
      Lists

      <v-btn
        :to="{
          name: 'bekpack-edit-trip',
          params: { tripId: trip.id },
        }"
        icon="mdi-plus"
      >
        +
      </v-btn>
    </v-toolbar>
    <div>
      {{ itemlists }}
    </div>
  </div>
</template>
<script lang="ts">
import { IPageRead } from "@/interfaces/common";
import { dispatchGetTrip } from "@/store/bekpack/actions";
import { readTripsOne } from "@/store/bekpack/getters";
import { dispatchGetBekpackItemlistMulti } from "@/store/bekpack/itemlist/actions";
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
  public get itemlists() {
    return readItemlistPage(this.$store);
  }
  public get tripId() {
    return +this.$router.currentRoute.params.tripId;
  }
  public get trip() {
    return readTripsOne(this.$store)(this.tripId);
  }
}
</script>

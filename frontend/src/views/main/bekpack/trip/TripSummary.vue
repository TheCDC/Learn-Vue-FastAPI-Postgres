<template>
  <div>
    <v-progress-circular :indeterminate="true" v-if="!trip">
    </v-progress-circular>
    <v-card :color="trip.color" v-if="trip">
      <v-card-title>
        {{ trip.name }}
      </v-card-title>
      <v-card-subtitle>
        Created: {{ localeDate(trip.time_created) }}

        Last modified : {{ localeDate(trip.time_updated) }}
      </v-card-subtitle>
      <v-card-text>
        {{ trip.description }}
      </v-card-text>
      <v-card-actions>
        <v-btn
          :to="{
            name: 'bekpack-edit-trip',
            params: { id: trip.id },
          }"
        >
          edit
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-toolbar dark dense color="gray"> Lists</v-toolbar>
  </div>
</template>
<script lang="ts">
import { dispatchGetTrip } from "@/store/bekpack/actions";
import { readTripsOne } from "@/store/bekpack/getters";
import { Component, Vue, Watch } from "vue-property-decorator";
@Component
export default class Bekpack extends Vue {
  public mounted() {
    dispatchGetTrip(this.$store, { id: this.tripId });
  }
  public get tripId() {
    return +this.$router.currentRoute.params.tripId;
  }
  public get trip() {
    return readTripsOne(this.$store)(this.tripId);
  }
}
</script>

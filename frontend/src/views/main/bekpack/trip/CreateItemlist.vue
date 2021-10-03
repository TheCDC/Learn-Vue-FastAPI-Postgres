<template>
  <v-container fluid>
    <v-card>
      <v-card-title primary-title>
        <div class="headline primary--text">Create Item List</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" @keyup.enter="submit" @submit.prevent="">
            <v-text-field
              @keyup.enter="submit"
              label="Title"
              v-model="title"
              required
            ></v-text-field>
            <v-color-picker v-model="color"> </v-color-picker>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { IBekpackItemListCreate } from "@/interfaces/bekpack.ts/bekpackitemlist";
import {
  dispatchCreateBekpackItemlist,
  dispatchGetBekpackItemlistMulti,
} from "@/store/bekpack/itemlist/actions";
import { Component, Vue } from "vue-property-decorator";

@Component
export default class BekpackTripCreate extends Vue {
  public title = "";
  public description = "";
  public quantity = 1;
  public color = "";
  public valid = false;

  public reset() {
    this.title = "";
    this.description = "";
    this.color = "";
  }
  public cancel() {
    this.$router.back();
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const newRecord: IBekpackItemListCreate = {
        name: this.title,
        color: this.color,
        parent_trip_id: +this.$router.currentRoute.params.tripId,
      };
      await dispatchCreateBekpackItemlist(this.$store, newRecord);
      await dispatchGetBekpackItemlistMulti(this.$store, {
        tripId: +this.$router.currentRoute.params.tripId,
        page: { page: 0, size: 64 },
      });
      this.$router.back();
    }
  }
}
</script>

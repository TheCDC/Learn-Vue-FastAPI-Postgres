<template>
  <v-container fluid>
    <v-card>
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Trip</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid">
            <v-text-field
              @keyup.enter="submit"
              label="Name"
              v-model="name"
              required
            ></v-text-field>
            <v-color-picker v-model="color"> </v-color-picker>

            <v-textarea
              label="Description"
              v-model="description"
              required
            ></v-textarea>
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
import { IBekpackTrip, IBekpackTripUpdate } from "@/interfaces";
import { IPage, IPageRead } from "@/interfaces/common";
import {
  dispatchGetMyTrips,
  dispatchGetTripToEdit,
  dispatchUpdateTrip,
} from "@/store/bekpack/actions";
import { readTripsOne, readTripToEdit } from "@/store/bekpack/getters";
import { Component, Vue } from "vue-property-decorator";
@Component
export default class EditItem extends Vue {
  public name = "";
  public description = "";
  public color = "";
  public valid = true;
  public async mounted() {
    await dispatchGetTripToEdit(this.$store, {
      id: +this.$router.currentRoute.params.id,
    });

    this.reset();
  }
  public cancel() {
    this.$router.back();
  }

  get item() {
    return readTripToEdit(this.$store);
  }
  public reset() {
    this.name = "";
    this.description = "";
    if (this.item) {
      this.name = this.item.name;
      this.description = this.item.description;
      this.color = this.item.color;
    }
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedTrip: IBekpackTripUpdate = {
        name: this.name,
        description: this.description,
        color: this.color,
      };
      await dispatchUpdateTrip(this.$store, {
        id: this.item!.id,
        item: updatedTrip,
      });
      this.$router.back();
    }
  }
}
</script>

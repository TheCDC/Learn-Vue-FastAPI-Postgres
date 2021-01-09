<template>
  <v-container fluid>
    <v-card>
      <v-card-title primary-title>
        <div class="headline primary--text">Create Trip</div>
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
            <v-color-picker> </v-color-picker>
            <v-textarea
              @keyup.enter="submit"
              label="Description"
              v-model="description"
              required
            ></v-textarea>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { IBekpackTripCreate } from "@/interfaces";
import { dispatchCreateTrip } from "@/store/bekpack/actions";
import { Component, Vue } from "vue-property-decorator";

@Component
export default class BekpackTripCreate extends Vue {
  public title = "";
  public description = "";
  public color = "";
  public valid = false;

  public reset() {
    this.title = "";
    this.description = "";
  }
  public cancel() {
    this.$router.back();
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const newTrip: IBekpackTripCreate = {
        name: this.title,
        description: this.description,
        color: this.color,
      };
      await dispatchCreateTrip(this.$store, newTrip);
      this.$router.push("/main/bekpack");
    }
  }
}
</script>

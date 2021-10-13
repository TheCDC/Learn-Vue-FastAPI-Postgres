<template>
  <v-container fluid>
    <v-card>
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Item List</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" @keyup.enter="submit" @submit.prevent="">
            <v-text-field
              @keyup.enter="submit"
              label="Name"
              v-model="name"
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
import {
  IBekpackItemList,
  IBekpackItemListUpdate,
} from "@/interfaces/bekpack.ts/bekpackitemlist";
import {
  dispatchDeleteBekpackItemlist,
  dispatchGetBekpackItemlist,
  dispatchGetBekpackItemlistMulti,
  dispatchUpdateBekpackItemlist,
} from "@/store/bekpack/itemlist/actions";
import { readItemlist } from "@/store/bekpack/itemlist/getters";
import { Component, Vue, Watch } from "vue-property-decorator";

@Component
export default class BekpackTripCreate extends Vue {
  public name = "";
  public description = "";
  public color = "";
  public valid = false;

  public reset() {
    this.name = "";
    this.description = "";
    this.color = "";
  }
  public cancel() {
    this.$router.back();
  }
  public mounted() {
    dispatchGetBekpackItemlist(this.$store, {
      id: this.itemId,
    });
  }
  public get itemId() {
    return +this.$router.currentRoute.params.itemlistId;
  }
  public get itemUnderEdit() {
    return readItemlist(this.$store)(this.itemId);
  }
  @Watch("itemUnderEdit")
  public onLoad(previous, next?: IBekpackItemList) {
    if (next) {
      this.name = next.name;
      this.color = next.color;
    }
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const newRecord: IBekpackItemListUpdate = {
        name: this.name,
        color: this.color,
      };
      dispatchUpdateBekpackItemlist(this.$store, {
        id: this.itemId,
        item: newRecord,
      });
      dispatchGetBekpackItemlistMulti(this.$store, {
        tripId: +this.$router.currentRoute.params.tripId,
        page: { page: 0, size: 64 },
      });
      this.$router.back();
    }
  }
}
</script>

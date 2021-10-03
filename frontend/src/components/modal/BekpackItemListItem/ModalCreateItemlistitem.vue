<template>
  <div>
    <v-dialog v-model="showDialog" width="500px ">
      <template v-slot:activator="{ attrs, on }">
        <slot :attrs="attrs" :on="on">
          <v-btn dark color="red lighten-2" light v-bind="attrs" v-on="on">
            Add Item
          </v-btn>
        </slot>
      </template>

      <v-card v-if="showDialog">
        <v-card-text>
          <template>
            <v-form v-model="valid">
              <v-layout column wrap>
                <v-text-field
                  label="Name"
                  v-model="name"
                  required
                  style="width: 90%"
                ></v-text-field>
              </v-layout>

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
          <v-btn color="primary" text @click="showDialog = false">
            Cancel
          </v-btn>
          <v-btn color="primary" text @click="reset">Reset</v-btn>
          <v-btn color="primary" @click="submit" :disabled="!valid">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { IBekpackItemListItemCreate } from "@/interfaces/bekpack.ts/bekpackitemlistitem";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class ModalCreateItemlistitem extends Vue {
  @Prop() public itemlistId!: number;
  public showDialog = false;
  public name = "";
  public description = "";

  public reset() {
    this.name = "";
    this.description = "";
  }

  public async mounted() {
    this.reset();
  }

  public cancel() {
    this.$router.back();
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const newRecord: IBekpackItemListItemCreate = {
        name: this.name,
        description: this.description,
      };

      this.reset();
      this.showDialog = false;
    }
  }
}
</script>

<template>
  <v-container fluid>
    <v-card>
      <v-card-title primary-title>
        <div class="headline primary--text">Create Item</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid">
            <v-text-field label="Title" v-model="title" required></v-text-field>
            <v-textarea
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
import { IItemCreate } from "@/interfaces";
import { dispatchCreateItem } from "@/store/item/actions";
import { Component, Vue } from "vue-property-decorator";

@Component
export default class ItemsCreate extends Vue {
  public title = "";
  public description = "";
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
      const newItem: IItemCreate = {
        title: this.title,
        description: this.description,
      };
      await dispatchCreateItem(this.$store, newItem);
      this.$router.push("/main/items");
    }
  }
}
</script>
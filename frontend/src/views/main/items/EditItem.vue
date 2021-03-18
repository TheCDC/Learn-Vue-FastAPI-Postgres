<template>
  <v-container fluid>
    <v-card>
      <v-card-title primary-title>
        <div class="headline primary--text">Edit Item</div>
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
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn @click="submit" :disabled="!valid">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
<script lang="ts">
import { IItem, IItemUpdate } from "@/interfaces";
import { dispatchGetItems, dispatchUpdateItem } from "@/store/item/actions";
import { readItemsOne } from "@/store/item/getters";
import { Component, Vue } from "vue-property-decorator";
@Component
export default class EditItem extends Vue {
  public title = "";
  public description = "";
  public valid = true;
  public async mounted() {
    await dispatchGetItems(this.$store);
    this.reset();
  }
  public cancel() {
    this.$router.back();
  }

  get item() {
    return readItemsOne(this.$store)(+this.$router.currentRoute.params.id);
  }
  public reset() {
    this.title = "";
    this.description = "";
    if (this.item) {
      this.title = this.item.title;
      this.description = this.item.description;
    }
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedItem: IItemUpdate = {
        title: this.title,
        description: this.description,
      };
      await dispatchUpdateItem(this.$store, {
        id: this.item!.id,
        item: updatedItem,
      });
      this.$router.push("/main/items");
    }
  }
}
</script>

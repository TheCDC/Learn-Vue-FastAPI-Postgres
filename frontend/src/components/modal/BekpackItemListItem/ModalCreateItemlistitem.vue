<template>
  <div>
    <v-dialog v-model="showDialog" width="500px ">
      <template v-slot:activator="{ attrs, on }">
        <slot :attrs="attrs" :on="on">
          <v-btn
            dark
            color="red lighten-2"
            light
            v-bind="attrs"
            v-on="on"
            v-if="!objectToEdit"
          >
            Add Item
          </v-btn>

          <v-btn light text v-bind="attrs" v-on="on" v-if="objectToEdit">
            <v-icon>edit</v-icon>
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
                  v-model="objectUnderEdit.name"
                  required
                  style="width: 90%"
                  autofocus
                ></v-text-field>
              </v-layout>

              <v-textarea
                label="Description"
                v-model="objectUnderEdit.description"
              ></v-textarea>
              <v-text-field
                label="Quantity"
                type="number"
                v-model="objectUnderEdit.quantity"
              >
              </v-text-field>
              <v-text-field
                label="List Index"
                type="number"
                v-model="objectUnderEdit.list_index"
              >
              </v-text-field>
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
import {
  IBekpackItemListItem,
  IBekpackItemListItemCreate,
} from "@/interfaces/bekpack.ts/bekpackitemlistitem";
import {
  dispatchCreateBekpackItemlistitem,
  dispatchGetBekpackItemlistitem,
  dispatchUpdateBekpackItemlistitem,
} from "@/store/bekpack/itemlistitem/actions";
import { readItemlistitem } from "@/store/bekpack/itemlistitem/getters";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class ModalCreateItemlistitem extends Vue {
  @Prop() public parentId!: number;
  @Prop() public onSuccess!: () => void;
  @Prop() public objectToEdit!: IBekpackItemListItem;
  public valid = false;
  public showDialog = false;
  public objectUnderEdit: IBekpackItemListItemCreate = {
    name: "",
    description: "",
    quantity: 1,
    list_index: 0,
    parent_list_id: this.parentId,
  };
  public reset() {
    if (!this.objectToEdit) {
      this.objectUnderEdit = {
        name: "",
        description: "",
        quantity: 1,
        list_index: 0,
        parent_list_id: this.parentId,
      };
    } else {
      this.objectUnderEdit = { ...this.objectToEdit };
    }
  }

  public async mounted() {
    this.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      if (!this.objectToEdit) {
        const newRecord: IBekpackItemListItemCreate = this.objectUnderEdit;
        await dispatchCreateBekpackItemlistitem(this.$store, newRecord);
      } else {
        await dispatchUpdateBekpackItemlistitem(this.$store, {
          id: this.objectToEdit.id,
          item: this.objectUnderEdit,
        });
      }
      this.onSuccess();
      this.reset();
      this.showDialog = false;
    }
  }
}
</script>

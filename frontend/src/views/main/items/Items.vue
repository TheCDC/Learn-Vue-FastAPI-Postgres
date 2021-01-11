<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title> Manage Your Items </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/items/create">Create Item</v-btn>
    </v-toolbar>
    <div>
      <v-data-table
        :headers="headers"
        :items="items"
        :footer-props="{
          showFirstLastPage: true,
        }"
      >
        <template v-slot:[`item.description`]="{ item }">
          {{ item.description | truncate(100, "...") }}
        </template>
        <template v-slot:[`item.title`]="{ item }">
          {{ item.title | truncate(100, "...") }}
        </template>

        <template v-slot:[`item.id`]="{ item }">
          <v-tooltip top>
            <span>Edit </span>
            <template v-slot:activator="{ on }">
              <v-btn
                text
                v-on="on"
                :to="{
                  name: 'main-items-edit',
                  params: { id: item.id },
                }"
                ><v-icon>edit</v-icon>
              </v-btn>
            </template>
          </v-tooltip>
          <v-tooltip top>
            <span>Delete </span>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on" text @click="deleteItem(item)"
                ><v-icon>delete</v-icon>
              </v-btn>
            </template>
          </v-tooltip>
        </template>
      </v-data-table>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { dispatchDeleteItem, dispatchGetItems } from "@/store/item/actions";
import { readItems, readItemsOneUser } from "@/store/item/getters";
import { readUserProfile } from "@/store/main/getters";
import { IItem } from "@/interfaces";
@Component
export default class Items extends Vue {
  public async mounted() {
    await dispatchGetItems(this.$store);
  }
  get items() {
    const user = readUserProfile(this.$store);
    if (user) {
      const x: IItem[] = readItems(this.$store);
      const ret = x;
      return ret;
    }
    return [];
  }
  get user() {
    return readUserProfile(this.$store);
  }
  public async deleteItem(item: IItem) {
    await dispatchDeleteItem(this.$store, item);
  }
  public headers = [
    { text: "title", sortable: true, value: "title", align: "left" },
    {
      text: "description",
      sortable: true,
      value: "description",
      align: "left",
    },
    { text: "Actions", sortable: false, value: "id" },
  ];
}
</script>

<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title> Manage Items </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/items/create">Create Item</v-btn>
    </v-toolbar>
    <v-container fluid>
      <div class="headline primary--text">Your Items, {{ user.full_name }}</div>
      <div>
        <v-data-table :headers="headers" :items="items">
          <template slot="items" slot-scope="props">
            <td>{{ props.item.title }}</td>
            <td>{{ props.item.description }}</td>
            <td>
              <v-tooltip top>
                <span>Edit </span>
                <v-btn
                  slot="activator"
                  flat
                  :to="{
                    name: 'main-items-edit',
                    params: { id: props.item.id },
                  }"
                  ><v-icon>edit</v-icon>
                </v-btn>
              </v-tooltip>
              <v-tooltip top>
                <span>Delete </span>
                <v-btn slot="activator" flat @click="deleteItem(props.item)"
                  ><v-icon>delete</v-icon>
                </v-btn>
              </v-tooltip>
            </td>
          </template>
        </v-data-table>
      </div>
    </v-container>
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
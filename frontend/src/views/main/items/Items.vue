<template>
  <v-container fluid>
    <div class="headline primary--text">Your Items, {{ user.full_name }}</div>
    <div>
      <v-data-table :headers="headers" :items="items">
        <template slot="items" slot-scope="props">
          <td>{{ props.item.title }}</td>
          <td>{{ props.item.description }}</td>
        </template>
      </v-data-table>
    </div>
  </v-container>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { dispatchGetItems } from "@/store/item/actions";
import { readItems, readItemsOneUser } from "@/store/item/getters";
import { readUserProfile } from "@/store/main/getters";
import { IItem } from "@/interfaces";
@Component
export default class Items extends Vue {
  public async mounted() {
    console.log("dispatchGetItems");
    await dispatchGetItems(this.$store);
    // await dispatchGetItems
  }
  get items() {
    const user = readUserProfile(this.$store);
    if (user) {
      const x: IItem[] = readItems(this.$store);
      console.log("readItems", x);
      const ret = x;
      return ret;
    }
    return [];
  }
  get user() {
    return readUserProfile(this.$store);
  }
  public headers = [
    { text: "title", sortable: true, value: "title" },
    { text: "description", sortable: true, value: "description" },
  ];
}
</script>
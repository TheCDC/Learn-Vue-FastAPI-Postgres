<template>
  <div>
    <v-progress-circular :indeterminate="true" v-if="!trip">
    </v-progress-circular>
    <div v-if="trip">
      <v-card :color="trip.color">
        <v-card-title class="d-flex flex-row justify-space-between flex-wrap">
          {{ trip.name }}
          <v-card-subtitle class="d-flex flex-row justify-start flex-wrap">
            <v-icon>face</v-icon> by {{ trip.owner.owner.full_name }} ({{
              trip.owner.owner.email
            }})
          </v-card-subtitle>
          <v-card-subtitle
            class="d-flex flex-row justify-space-between flex-wrap"
          >
            <v-icon>schedule</v-icon> Modified :
            {{ trip.time_updated | localeDate }}
          </v-card-subtitle>

          <v-card-subtitle>
            <v-icon>update</v-icon>
            Created: {{ trip.time_created | localeDate }}
          </v-card-subtitle>
        </v-card-title>

        <v-card-text>
          {{ trip.description }}
        </v-card-text>
        <v-card-actions>
          <v-btn
            :to="{
              name: 'bekpack-edit-trip',
              params: { tripId: trip.id },
            }"
          >
            edit
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-tabs v-model="tab">
        <v-tab>
          Lists

          <v-icon>assignment</v-icon>
        </v-tab>
        <v-tab>
          Bags

          <v-icon> backpack </v-icon>
        </v-tab>
      </v-tabs>
    </div>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-toolbar dark color="gray">
          <v-btn
            light
            :to="{
              name: 'bekpack-create-itemlist',
              params: { tripId: trip.id },
            }"
          >
            Create List +
          </v-btn>
        </v-toolbar>
        <div class="d-flex flex-row justify-start flex-wrap">
          <v-card
            v-for="itemlist in itemlistsPage.items"
            :key="itemlist.id"
            class="ma-2"
          >
            <v-toolbar :color="itemlist.color">
              <div width="auto"></div>
              <v-btn
                class="ma-auto"
                dense
                text
                :to="{
                  name: 'bekpack-edit-itemlist',
                  params: { itemlistId: itemlist.id },
                }"
              >
                <v-icon> edit </v-icon>
              </v-btn>
              <v-toolbar-title class="flex-grow-1 justify-space-around">
                <div>
                  {{ itemlist.name }}
                </div>
              </v-toolbar-title>
              <v-btn text class="ma-auto" dense @click="deleteChild(itemlist)">
                <v-icon> delete </v-icon>
              </v-btn>
            </v-toolbar>
            <v-card-text>
              <div class="d-flex flex-row justify-start flex-nowrap ma-2">
                <v-btn
                  :to="{
                    name: 'bekpack-edit-itemlist',
                    params: { itemlistId: itemlist.id },
                  }"
                >
                  <v-icon> edit </v-icon>
                </v-btn>
                <v-spacer />
                <v-btn @click="deleteChild(itemlist)">
                  <v-icon> delete </v-icon>
                </v-btn>
              </div>
              <v-data-table
                v-if="itemlist.items.length > 0"
                :items="itemlist.items"
                :headers="[
                  { text: 'Name', value: 'name' },
                  { text: 'Quantity', value: 'quantity' },
                  { text: 'Bag' },
                  { text: 'Status' },
                  { text: '', value: 'id' },
                ]"
                :disable-pagination="true"
                :hide-default-footer="true"
              >
                <template v-slot:[`item.name`]="{ item }">
                  <div class="d-flex flex-row justify-start flex-nowrap">
                    <modal-create-itemlistitem
                      :onSuccess="refresh"
                      :parentId="itemlist.id"
                      :objectToEdit="item"
                    >
                    </modal-create-itemlistitem>
                    <div class="ma-auto">
                      {{ item.name }}
                    </div>
                  </div>
                </template>
                <template v-slot:[`item.id`]="{ item }">
                  <v-btn @click="deleteChildChild(item)" text small dense>
                    <v-icon> delete </v-icon>
                  </v-btn>
                </template>
              </v-data-table>
              <modal-create-itemlistitem
                :onSuccess="refresh"
                :parentId="itemlist.id"
              >
              </modal-create-itemlistitem>
            </v-card-text>
          </v-card>
        </div>
      </v-tab-item>
      <v-tab-item> BAGS UNDER CONSTRUCTION </v-tab-item>
    </v-tabs-items>
  </div>
</template>
<script lang="ts">
import ModalCreateItemlistitem from "@/components/modal/BekpackItemListItem/ModalCreateItemlistitem.vue";
import { IBekpackItemList } from "@/interfaces/bekpack.ts/bekpackitemlist";
import { IBekpackItemListItem } from "@/interfaces/bekpack.ts/bekpackitemlistitem";
import { IPageRead } from "@/interfaces/common";
import { dispatchGetTrip } from "@/store/bekpack/actions";
import { readTripsOne } from "@/store/bekpack/getters";
import {
  dispatchDeleteBekpackItemlist,
  dispatchGetBekpackItemlistMulti,
} from "@/store/bekpack/itemlist/actions";
import { readItemlistPage } from "@/store/bekpack/itemlist/getters";
import { dispatchDeleteBekpackItemlistitem } from "@/store/bekpack/itemlistitem/actions";
import { Component, Vue } from "vue-property-decorator";
@Component({ components: { ModalCreateItemlistitem } })
export default class Bekpack extends Vue {
  public pageCursor: IPageRead = { page: 0, size: 64 };
  public tab = null;
  public mounted() {
    this.refresh();
  }
  public get itemlistsPage() {
    return readItemlistPage(this.$store);
  }
  public get tripId() {
    return +this.$router.currentRoute.params.tripId;
  }
  public get trip() {
    return readTripsOne(this.$store)(this.tripId);
  }
  public async refreshChildren() {
    dispatchGetBekpackItemlistMulti(this.$store, {
      tripId: this.tripId,
      page: this.pageCursor,
    });
  }
  public async refresh() {
    dispatchGetTrip(this.$store, { id: this.tripId });
    this.refreshChildren();
  }
  public async deleteChildChild(o: IBekpackItemListItem) {
    await dispatchDeleteBekpackItemlistitem(this.$store, o);
    this.refreshChildren();
  }
  public async deleteChild(item: IBekpackItemList) {
    await dispatchDeleteBekpackItemlist(this.$store, item);
    dispatchGetBekpackItemlistMulti(this.$store, {
      tripId: this.tripId,
      page: this.pageCursor,
    });
  }
}
</script>

import { IBekpackTrip, IBekpackUser } from "@/interfaces";
import { IBekpackItemList } from "@/interfaces/bekpack.ts/bekpackitemlist";
import { IPage } from "@/interfaces/common";

export interface BekpackItemListState {
  itemlists: IBekpackItemList[];
  itemlistPage: IPage<IBekpackItemList>;
}

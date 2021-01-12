import { IBekpackUser, IBekpackTrip } from '@/interfaces';
import { IPage } from '@/interfaces/common';

export interface BekpackState {
    user: IBekpackUser | null;
    trips: IPage<IBekpackTrip>;
    tripToEdit: IBekpackTrip | null;
    hasBekpackAccount: boolean | null;
}

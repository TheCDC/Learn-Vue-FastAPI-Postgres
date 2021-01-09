import { IBekpackUser, IBekpackTrip } from '@/interfaces';

export interface BekpackState {
    user: IBekpackUser | null;
    trips: IBekpackTrip[];
    hasBekpackAccount: boolean | null;
}

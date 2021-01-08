import { IBekpackUser, IBekpackTrip } from '@/interfaces';

export interface BekpackState {
    users: IBekpackUser[];
    trips: IBekpackTrip[];
}

import { EventDto } from 'src/app/models/event.model';

export interface EventState {
  events: EventDto[];
}

export const initialEventState: EventState = {
  events: [],
};

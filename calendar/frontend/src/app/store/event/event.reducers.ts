import { createReducer, on } from '@ngrx/store';
import { initialEventState, EventState } from './event.state';
import * as A from './event.actions';

export const eventReducer = createReducer(
  initialEventState,
  on(
    A.getEventsOk,
    (state, { events }): EventState => ({
      ...state,
      events,
    }),
  ),
  on(
    A.createEventOk,
    (state, { event }): EventState => ({
      ...state,
      events: [...(state?.events ?? []), event],
    }),
  ),
  on(
    A.updateEventOk,
    (state, { event }): EventState => ({
      ...state,
      events: state.events?.map((x) => (x.id === event.id ? event : x)),
    }),
  ),
  on(
    A.deleteEventOk,
    (state, { id }): EventState => ({
      ...state,
      events: state.events?.filter((x) => x.id !== id),
    }),
  ),
);

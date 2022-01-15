import { createAction, props } from '@ngrx/store';
import { EventDto } from 'src/app/models/event.model';

export const getEvents = createAction('[Event] Get events', props<{ from: Date; to: Date }>());
export const getEventsOk = createAction('[Event] Get events Ok', props<{ events: EventDto[] }>());

export const createEvent = createAction('[Event] Create event', props<{ event: EventDto }>());
export const createEventOk = createAction('[Event] Create event Ok', props<{ event: EventDto }>());

export const updateEvent = createAction('[Event] Update event', props<{ event: EventDto }>());
export const updateEventOk = createAction('[Event] Update event Ok', props<{ event: EventDto }>());

export const deleteEvent = createAction('[Event] Delete event', props<{ id: number }>());
export const deleteEventOk = createAction('[Event] Delete event Ok', props<{ id: number }>());

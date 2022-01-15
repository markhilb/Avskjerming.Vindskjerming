import { createSelector } from '@ngrx/store';
import { selectAppState } from '../app.reducers';

export const selectEventState = createSelector(selectAppState, (state) => state.eventState);

export const selectEvents = createSelector(selectEventState, (state) => state.events);

// const serializeEvent = (event: CalendarEvent<MetaData>): EventDto => ({
//   id: event.meta?.id ?? 0,
//   title: event.title,
//   details: event.meta?.details ?? '',
//   start: event.start,
//   end: event.end ?? event.start,
//   teamId: event.meta?.team.id ?? 0,
//   team: event.meta?.team ?? ({ id: 0 } as TeamDto),
//   employees: event.meta?.employees ?? [],
// });

export const selectCalendarEvents = createSelector(selectEvents, (state) =>
  state.map((event) => ({
    start: event.start,
    end: event.end,
    title: event.title,
    color: event.team
      ? { primary: event.team.primaryColor, secondary: event.team.secondaryColor }
      : { primary: '#ffffff', secondary: '#aaaaaa' },
    resizable: {
      beforeStart: true,
      afterEnd: true,
    },
    draggable: true,
    meta: {
      details: event.details,
      team: event.team,
      employees: event.employees,
      id: event.id,
    },
  })),
);

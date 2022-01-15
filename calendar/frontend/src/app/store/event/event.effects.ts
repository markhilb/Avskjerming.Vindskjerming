import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, exhaustMap, map, switchMap } from 'rxjs/operators';
import { EventService } from 'src/app/services/api/event.service';
import { ToastService } from 'src/app/services/toast.service';
import * as A from './event.actions';

@Injectable()
export class EventEffects {
  getEvents$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.getEvents),
      switchMap((action) =>
        this.eventService.getEvents(action.from, action.to).pipe(
          map((events) => A.getEventsOk({ events })),
          catchError((error) => this.toastService.error(error)),
        ),
      ),
    ),
  );

  createEvent$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.createEvent),
      exhaustMap((action) =>
        this.eventService.createEvent(action.event).pipe(
          map((id) => A.createEventOk({ event: { ...action.event, id } })),
          catchError((error) => this.toastService.error(error)),
        ),
      ),
    ),
  );

  updateEvent$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.updateEvent),
      exhaustMap((action) =>
        this.eventService.updateEvent(action.event).pipe(
          map(() => A.updateEventOk(action)),
          catchError((error) => this.toastService.error(error)),
        ),
      ),
    ),
  );

  deleteEvent$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.deleteEvent),
      exhaustMap((action) =>
        this.eventService.deleteEvent(action.id).pipe(
          map(() => A.deleteEventOk(action)),
          catchError((error) => this.toastService.error(error)),
        ),
      ),
    ),
  );

  constructor(private actions: Actions, private eventService: EventService, private toastService: ToastService) {}
}

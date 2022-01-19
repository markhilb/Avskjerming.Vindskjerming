import { Component, ElementRef, HostListener, TemplateRef, ViewChild } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { CalendarEvent, CalendarEventTimesChangedEvent, CalendarView } from 'angular-calendar';
import { addDays, addHours, endOfDay, endOfWeek, isSameWeek, startOfDay, startOfWeek } from 'date-fns';
import { EmployeeDto, EventDto, TeamDto } from 'src/app/models/event.model';
import {
  AppState,
  createEvent,
  deleteEvent,
  getEmployees,
  getEvents,
  selectAvailableEmployees,
  selectCalendarEvents,
  selectEmployees,
  updateEvent,
} from 'src/app/store';
import { Store } from '@ngrx/store';
import { getTeams, selectTeams } from 'src/app/store/team';
import { interval } from 'rxjs';
import { UntilDestroy, untilDestroyed } from '@ngneat/until-destroy';

interface MetaData {
  id: number;
  details: string;
  team: TeamDto | null;
  employees: EmployeeDto[];
}

const serializeEvent = (event: CalendarEvent<MetaData>): EventDto => ({
  id: event.meta?.id ?? 0,
  title: event.title,
  details: event.meta?.details ?? '',
  start: event.start,
  end: event.end ?? event.start,
  teamId: event.meta?.team?.id ?? null,
  team: event.meta?.team ?? null,
  employees: event.meta?.employees ?? [],
});

const _createEvent = (start: Date, end: Date) =>
  ({
    start,
    end,
    title: '',
    color: { primary: 'red', secondary: 'green' },
    resizable: {
      beforeStart: true,
      afterEnd: true,
    },
    draggable: true,
    meta: {
      details: '',
      team: null,
      employees: [],
      id: 0,
    },
  } as CalendarEvent<MetaData>);

@UntilDestroy()
@Component({
  selector: 'app-calendar-page',
  templateUrl: './calendar-page.component.html',
  styleUrls: ['./calendar-page.component.scss'],
})
export class CalendarPageComponent {
  @ViewChild('modalContent', { static: true }) modalContent?: TemplateRef<any>;
  @ViewChild('next', { static: false }) next?: ElementRef;
  @ViewChild('previous', { static: false }) previous?: ElementRef;
  @ViewChild('today', { static: false }) today?: ElementRef;

  dayStart = 7;
  dayEnd = 22;
  excludeDays = [0, 6];

  CalendarView = CalendarView;
  view = window.innerWidth < 500 ? CalendarView.Day : CalendarView.Week;

  startOfWeek = startOfWeek;
  addDays = addDays;

  currentWeek = new Date();

  viewDate = new Date();
  get nextWeekDate() {
    return addDays(this.viewDate, 7);
  }

  modalData = {} as CalendarEvent;

  events$ = this.store.select(selectCalendarEvents);
  teams$ = this.store.select(selectTeams);
  employees$ = this.store.select(selectEmployees);

  constructor(private store: Store<AppState>, private modal: NgbModal) {
    this.fetchEvents();
    interval(1000 * 60 * 5)
      .pipe(untilDestroyed(this))
      .subscribe(() => this.fetchEvents());

    store.dispatch(getTeams());
    store.dispatch(getEmployees());

    interval(5000 * 60 * 60)
      .pipe(untilDestroyed(this))
      .subscribe(() => {
        if (!isSameWeek(new Date(), this.currentWeek)) {
          this.currentWeek = new Date();
          this.viewDate = this.nextWeekDate;
          this.fetchEvents();
        }
      });
  }

  @HostListener('document:keydown', ['$event']) keydown(event: KeyboardEvent) {
    if (!this.modal.hasOpenModals()) {
      if (event.key == 'ArrowRight') {
        this.next?.nativeElement.click();
      } else if (event.key === 'ArrowLeft') {
        this.previous?.nativeElement.click();
      } else if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
        this.today?.nativeElement.click();
      } else if (event.key === 'Tab') {
        this.newEvent({ date: new Date() });
        event.preventDefault();
      }
    } else {
      if (event.key === 'Escape') {
        this.modal.dismissAll();
      }
    }
  }

  fetchEvents() {
    this.store.dispatch(
      getEvents(
        this.view === CalendarView.Day
          ? { from: startOfDay(this.viewDate), to: endOfDay(this.viewDate) }
          : this.view === CalendarView.Week
          ? { from: startOfWeek(this.viewDate), to: endOfWeek(this.viewDate) }
          : { from: startOfWeek(this.viewDate), to: endOfWeek(this.nextWeekDate) },
      ),
    );
  }

  availableEmployees(event: CalendarEvent) {
    return this.store.select(selectAvailableEmployees(event));
  }

  eventTimesChanged({ event, newStart, newEnd }: CalendarEventTimesChangedEvent): void {
    this.store.dispatch(updateEvent({ event: serializeEvent({ ...event, start: newStart, end: newEnd }) }));
  }

  newEvent({ date }: { date: Date }) {
    const event = _createEvent(date, addHours(date, 1));
    this.openModal(event);
    (document.getElementById('title') as HTMLElement).focus();
  }

  confirmNewEvent() {
    this.store.dispatch(createEvent({ event: serializeEvent(this.modalData) }));
    this.modal.dismissAll();
  }

  updateEvent() {
    this.store.dispatch(updateEvent({ event: serializeEvent(this.modalData) }));
    this.modal.dismissAll();
  }

  openModal(event: CalendarEvent): void {
    this.modalData = { ...event, meta: { ...event.meta } };
    this.modal.open(this.modalContent, { size: 'lg', centered: true });
  }

  deleteEvent(event: CalendarEvent) {
    this.store.dispatch(deleteEvent({ id: event.meta.id }));
    this.modal.dismissAll();
  }

  changeTeam(team: TeamDto) {
    this.modalData.meta.team = team;
    this.modalData.color = { primary: team.primaryColor, secondary: team.secondaryColor };
  }

  removeEmployee(employee: EmployeeDto) {
    this.modalData.meta.employees = this.modalData.meta.employees.filter((e: EmployeeDto) => e.id !== employee.id);
  }

  addEmployee(event: EmployeeDto) {
    this.modalData.meta.employees = [...this.modalData.meta.employees, event];
  }
}

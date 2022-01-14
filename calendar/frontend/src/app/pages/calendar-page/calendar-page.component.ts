import { Component, ElementRef, HostListener, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { CalendarEvent, CalendarEventTimesChangedEvent, CalendarView } from 'angular-calendar';
import { addDays, addHours, startOfWeek } from 'date-fns';
import { Subject } from 'rxjs';
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

interface MetaData {
  id: number;
  details: string;
  team: TeamDto;
  employees: EmployeeDto[];
}

const serializeEvent = (event: CalendarEvent<MetaData>): EventDto => ({
  id: event.meta?.id ?? 0,
  title: event.title,
  details: event.meta?.details ?? '',
  start: event.start,
  end: event.end ?? event.start,
  teamId: event.meta?.team.id ?? 0,
  team: event.meta?.team ?? ({ id: 0 } as TeamDto),
  employees: event.meta?.employees ?? [],
});

const _createEvent = (start: Date, end: Date) =>
  ({
    start,
    end,
    title: '',
    resizable: {
      beforeStart: true,
      afterEnd: true,
    },
    draggable: true,
    meta: {
      details: '',
      team: {} as TeamDto,
      employees: [],
      id: 0,
    },
  } as CalendarEvent<MetaData>);

@Component({
  selector: 'app-calendar-page',
  templateUrl: './calendar-page.component.html',
  styleUrls: ['./calendar-page.component.scss'],
})
export class CalendarPageComponent implements OnInit {
  @ViewChild('modalContent', { static: true }) modalContent?: TemplateRef<any>;
  @ViewChild('next', { static: false }) next?: ElementRef;
  @ViewChild('previous', { static: false }) previous?: ElementRef;
  @ViewChild('today', { static: false }) today?: ElementRef;

  dayStart = 8;
  dayEnd = 17;
  excludeDays = [0, 6];

  CalendarView = CalendarView;
  view = window.innerWidth < 500 ? CalendarView.Day : CalendarView.Week;

  startOfWeek = startOfWeek;
  addDays = addDays;

  viewDate = new Date();
  get nextWeekDate() {
    return addDays(this.viewDate, 7);
  }

  modalData = {} as CalendarEvent;

  refresh$ = new Subject<void>();

  events$ = this.store.select(selectCalendarEvents);
  teams$ = this.store.select(selectTeams);
  employees$ = this.store.select(selectEmployees);

  zoom = 1;
  @HostListener('window:resize', [])
  onResize() {
    // const header = document.getElementById('header') as HTMLElement;
    // const div = document.getElementById('calendar-body') as HTMLElement;
    // setTimeout(() => {
    //   this.zoom = (window.innerHeight - header.offsetHeight) / div.offsetHeight;
    //   if (this.zoom < 1) this.zoom = 1;
    // }, 0);
  }

  constructor(private store: Store<AppState>, private modal: NgbModal) {
    store.dispatch(getEvents());
    store.dispatch(getTeams());
    store.dispatch(getEmployees());
  }

  ngOnInit(): void {
    this.onResize();
  }

  @HostListener('document:keydown', ['$event']) keydown(event: KeyboardEvent) {
    if (event.key == 'ArrowRight') {
      this.next?.nativeElement.click();
    } else if (event.key === 'ArrowLeft') {
      this.previous?.nativeElement.click();
    } else if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
      this.today?.nativeElement.click();
    }
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
    this.modalData = { ...event };
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

  changeView(view: CalendarView) {
    this.view = view;
    this.onResize();
  }

  removeEmployee(employee: EmployeeDto) {
    this.modalData.meta.employees = this.modalData.meta.employees.filter((e: EmployeeDto) => e.id !== employee.id);
  }

  addEmployee(event: EmployeeDto) {
    this.modalData.meta.employees = [...this.modalData.meta.employees, event];
  }
}

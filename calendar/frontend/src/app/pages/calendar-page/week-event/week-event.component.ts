import { Component, EventEmitter, Input, Output, TemplateRef } from '@angular/core';
import { PlacementArray } from '@ng-bootstrap/ng-bootstrap/util/positioning';
import { WeekViewAllDayEventResize } from 'angular-calendar/modules/week/calendar-week-view.component';
import { WeekViewHourColumn, WeekViewTimeEvent } from 'calendar-utils';
import { EmployeeDto } from 'src/app/models/event.model';

@Component({
  selector: 'app-week-event',
  templateUrl: './week-event.component.html',
  styleUrls: ['./week-event.component.scss'],
})
export class WeekEventComponent {
  @Input() locale: string;

  @Input() weekEvent: WeekViewAllDayEventResize | WeekViewTimeEvent;

  @Input() tooltipPlacement: PlacementArray;

  @Input() tooltipAppendToBody: boolean;

  @Input() tooltipDisabled: boolean;

  @Input() tooltipDelay: number | null;

  @Input() customTemplate: TemplateRef<any>;

  @Input() eventTitleTemplate: TemplateRef<any>;

  @Input() eventActionsTemplate: TemplateRef<any>;

  @Input() tooltipTemplate: TemplateRef<any>;

  @Input() column: WeekViewHourColumn;

  @Input() daysInWeek: number;

  @Output() eventClicked = new EventEmitter<{
    sourceEvent: MouseEvent | KeyboardEvent;
  }>();

  get tooltipContent() {
    const event = (this.weekEvent as WeekViewTimeEvent).event;
    let content = `<div>${event.title.toUpperCase()}</div>`;

    if (event.meta.details) content += `<div>${event.meta.details}</div>`;

    if (event.meta.employees?.length)
      content += `<div>${event.meta.employees.map((e: EmployeeDto) => `<span>${e.name}</span>`)}</div>`;

    return content;
  }
}

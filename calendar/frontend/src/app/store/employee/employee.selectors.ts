import { createSelector } from '@ngrx/store';
import { CalendarEvent } from 'angular-calendar';
import { selectAppState } from '../app.reducers';
import { EmployeeDto } from 'src/app/models/event.model';

export const selectEmployeeState = createSelector(selectAppState, (state) => state.employeeState);

export const selectEmployees = createSelector(selectEmployeeState, (state) => state.employees);
export const selectAvailableEmployees = (event: CalendarEvent) =>
  createSelector(selectEmployees, (state) =>
    state.filter((employee) => !event.meta.employees.some((_e: EmployeeDto) => _e.id === employee.id)),
  );

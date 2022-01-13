import { createAction, props } from '@ngrx/store';
import { EmployeeDto } from 'src/app/models/event.model';

export const getEmployees = createAction('[Employee] Get employees');
export const getEmployeesOk = createAction('[Employee] Get employees Ok', props<{ employees: EmployeeDto[] }>());

export const createEmployee = createAction('[Employee] Create employee', props<{ employee: EmployeeDto }>());
export const createEmployeeOk = createAction('[Employee] Create employee Ok', props<{ employee: EmployeeDto }>());

export const updateEmployee = createAction('[Employee] Update employee', props<{ employee: EmployeeDto }>());
export const updateEmployeeOk = createAction('[Employee] Update employee Ok', props<{ employee: EmployeeDto }>());

export const deleteEmployee = createAction('[Employee] Delete employee', props<{ id: number }>());
export const deleteEmployeeOk = createAction('[Employee] Delete employee Ok', props<{ id: number }>());

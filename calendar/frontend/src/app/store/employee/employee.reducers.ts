import { createReducer, on } from '@ngrx/store';
import { initialEmployeeState, EmployeeState } from './employee.state';
import * as A from './employee.actions';

export const employeeReducer = createReducer(
  initialEmployeeState,
  on(
    A.getEmployeesOk,
    (state, { employees }): EmployeeState => ({
      ...state,
      employees,
    }),
  ),
  on(
    A.createEmployeeOk,
    (state, { employee }): EmployeeState => ({
      ...state,
      employees: [...(state?.employees ?? []), employee],
    }),
  ),
  on(
    A.updateEmployeeOk,
    (state, { employee }): EmployeeState => ({
      ...state,
      employees: state.employees?.map((x) => (x.id === employee.id ? employee : x)),
    }),
  ),
  on(
    A.deleteEmployeeOk,
    (state, { id }): EmployeeState => ({
      ...state,
      employees: state.employees?.filter((x) => x.id !== id),
    }),
  ),
);

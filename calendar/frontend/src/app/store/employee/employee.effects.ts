import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { EMPTY } from 'rxjs';
import { catchError, exhaustMap, map, switchMap } from 'rxjs/operators';
import { EmployeeService } from 'src/app/services/api/employee.service';
import * as A from './employee.actions';

@Injectable()
export class EmployeeEffects {
  getEmployees$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.getEmployees),
      switchMap(() =>
        this.employeeService.getEmployees().pipe(
          map((employees) => A.getEmployeesOk({ employees })),
          catchError(() => EMPTY),
        ),
      ),
    ),
  );

  createEmployee$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.createEmployee),
      exhaustMap((action) =>
        this.employeeService.createEmployee(action.employee).pipe(
          map((id) => A.createEmployeeOk({ employee: { ...action.employee, id } })),
          catchError(() => EMPTY),
        ),
      ),
    ),
  );

  updateEmployee$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.updateEmployee),
      exhaustMap((action) =>
        this.employeeService.updateEmployee(action.employee).pipe(
          map(() => A.updateEmployeeOk(action)),
          catchError(() => EMPTY),
        ),
      ),
    ),
  );

  deleteEmployee$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.deleteEmployee),
      exhaustMap((action) =>
        this.employeeService.deleteEmployee(action.id).pipe(
          map(() => A.deleteEmployeeOk(action)),
          catchError(() => EMPTY),
        ),
      ),
    ),
  );

  constructor(private actions: Actions, private employeeService: EmployeeService) {}
}

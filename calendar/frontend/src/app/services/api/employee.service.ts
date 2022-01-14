import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { EmployeeDto } from 'src/app/models/event.model';
import { BaseApiService } from './base-api.service';

@Injectable({
  providedIn: 'root',
})
export class EmployeeService {
  constructor(private api: BaseApiService) {}

  getEmployees = (): Observable<EmployeeDto[]> => this.api.get<EmployeeDto[]>('Employees');

  createEmployee = (event: EmployeeDto): Observable<number> => this.api.post<number>('Employees', event);

  updateEmployee = (event: EmployeeDto): Observable<boolean> => this.api.put<boolean>('Employees', {}, event);

  deleteEmployee = (id: number): Observable<boolean> => this.api.delete<boolean>('Employees/' + id);
}

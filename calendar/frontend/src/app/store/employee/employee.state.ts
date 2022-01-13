import { EmployeeDto } from 'src/app/models/event.model';

export interface EmployeeState {
  employees: EmployeeDto[];
}

export const initialEmployeeState: EmployeeState = {
  employees: [],
};

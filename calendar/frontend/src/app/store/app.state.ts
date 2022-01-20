import { EventState, initialEventState } from '.';
import { EmployeeState, initialEmployeeState } from './employee';
import { initialTeamState, TeamState } from './team';

export interface AppState {
  eventState: EventState;
  teamState: TeamState;
  employeeState: EmployeeState;
}

export const initialAppState: AppState = {
  eventState: initialEventState,
  teamState: initialTeamState,
  employeeState: initialEmployeeState,
};

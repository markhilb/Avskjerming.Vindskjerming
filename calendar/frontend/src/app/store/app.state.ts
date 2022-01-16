import { AuthenticationState, EventState, initialAuthenticationState, initialEventState } from '.';
import { EmployeeState, initialEmployeeState } from './employee';
import { initialTeamState, TeamState } from './team';

export interface AppState {
  eventState: EventState;
  teamState: TeamState;
  employeeState: EmployeeState;
  authenticationState: AuthenticationState;
}

export const initialAppState: AppState = {
  eventState: initialEventState,
  teamState: initialTeamState,
  employeeState: initialEmployeeState,
  authenticationState: initialAuthenticationState,
};

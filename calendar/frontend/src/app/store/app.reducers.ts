import { Action, ActionReducer, ActionReducerMap, createSelector } from '@ngrx/store';
import { logoutOk } from '.';
import { AppState } from './app.state';
import { authenticationReducer } from './authentication/authentication.reducers';
import { employeeReducer } from './employee/employee.reducers';
import { eventReducer } from './event/event.reducers';
import { teamReducer } from './team/team.reducers';

export const appReducers: ActionReducerMap<AppState, any> = {
  eventState: eventReducer,
  teamState: teamReducer,
  employeeState: employeeReducer,
  authenticationState: authenticationReducer,
};

const appState = (state: AppState) => state;
export const selectAppState = createSelector(appState, (state) => state);

const resetState = (reducer: ActionReducer<AppState>) => (state: AppState | undefined, action: Action) =>
  action.type === logoutOk.type
    ? reducer({ authenticationState: { isLoggedIn: false } } as any, action)
    : reducer(state, action);

export const metaReducers = [resetState];

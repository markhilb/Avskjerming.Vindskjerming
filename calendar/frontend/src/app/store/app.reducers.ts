import { ActionReducerMap, createSelector } from '@ngrx/store';
import { AppState } from './app.state';
import { employeeReducer } from './employee/employee.reducers';
import { eventReducer } from './event/event.reducers';
import { teamReducer } from './team/team.reducers';

export const appReducers: ActionReducerMap<AppState, any> = {
  eventState: eventReducer,
  teamState: teamReducer,
  employeeState: employeeReducer,
};

const appState = (state: AppState) => state;
export const selectAppState = createSelector(appState, (state) => state);

import { createSelector } from '@ngrx/store';
import { selectAppState } from '../app.reducers';

export const selectTeamState = createSelector(selectAppState, (state) => state.teamState);

export const selectTeams = createSelector(selectTeamState, (state) => state.teams);

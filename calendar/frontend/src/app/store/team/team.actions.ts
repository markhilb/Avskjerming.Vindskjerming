import { createAction, props } from '@ngrx/store';
import { TeamDto } from 'src/app/models/event.model';

export const getTeams = createAction('[Team] Get teams');
export const getTeamsOk = createAction('[Team] Get teams Ok', props<{ teams: TeamDto[] }>());

export const createTeam = createAction('[Team] Create team', props<{ team: TeamDto }>());
export const createTeamOk = createAction('[Team] Create team Ok', props<{ team: TeamDto }>());

export const updateTeam = createAction('[Team] Update team', props<{ team: TeamDto }>());
export const updateTeamOk = createAction('[Team] Update team Ok', props<{ team: TeamDto }>());

export const deleteTeam = createAction('[Team] Delete team', props<{ id: number }>());
export const deleteTeamOk = createAction('[Team] Delete team Ok', props<{ id: number }>());

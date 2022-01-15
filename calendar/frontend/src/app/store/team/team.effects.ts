import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { EMPTY } from 'rxjs';
import { catchError, exhaustMap, map, switchMap } from 'rxjs/operators';
import { TeamService } from 'src/app/services/api/team.service';
import * as A from './team.actions';

@Injectable()
export class TeamEffects {
  getTeams$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.getTeams),
      switchMap(() =>
        this.teamService.getTeams().pipe(
          map((teams) => A.getTeamsOk({ teams })),
          catchError(() => EMPTY),
        ),
      ),
    ),
  );

  createTeam$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.createTeam),
      exhaustMap((action) =>
        this.teamService.createTeam(action.team).pipe(
          map((id) => A.createTeamOk({ team: { ...action.team, id } })),
          catchError(() => EMPTY),
        ),
      ),
    ),
  );

  updateTeam$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.updateTeam),
      exhaustMap((action) =>
        this.teamService.updateTeam(action.team).pipe(
          map(() => A.updateTeamOk(action)),
          catchError(() => EMPTY),
        ),
      ),
    ),
  );

  deleteTeam$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.deleteTeam),
      exhaustMap((action) =>
        this.teamService.deleteTeam(action.id).pipe(
          map(() => A.deleteTeamOk(action)),
          catchError(() => EMPTY),
        ),
      ),
    ),
  );

  constructor(private actions: Actions, private teamService: TeamService) {}
}

import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { TeamDto } from 'src/app/models/event.model';
import { BaseApiService } from './base-api.service';

@Injectable({
  providedIn: 'root',
})
export class TeamService {
  constructor(private api: BaseApiService) {}

  getTeams = (): Observable<TeamDto[]> => this.api.get<TeamDto[]>('Teams');

  createTeam = (event: TeamDto): Observable<number> => this.api.post<number>('Teams', event);

  updateTeam = (event: TeamDto): Observable<boolean> => this.api.put<boolean>('Teams', {}, event);

  deleteTeam = (id: number): Observable<boolean> => this.api.delete<boolean>('Teams/' + id);
}

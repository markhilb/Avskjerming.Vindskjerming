import { TeamDto } from 'src/app/models/event.model';

export interface TeamState {
  teams: TeamDto[];
}

export const initialTeamState: TeamState = {
  teams: [],
};

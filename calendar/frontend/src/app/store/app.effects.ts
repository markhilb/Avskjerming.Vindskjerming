import { EmployeeEffects } from './employee/employee.effects';
import { EventEffects } from './event/event.effects';
import { TeamEffects } from './team/team.effects';

export const appEffects = [EventEffects, TeamEffects, EmployeeEffects];

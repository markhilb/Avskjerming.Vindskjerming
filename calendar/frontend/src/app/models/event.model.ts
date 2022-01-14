export interface EventDto {
  id: number;
  title: string;
  details: string;
  start: Date;
  end: Date;
  teamId: number;
  team: TeamDto;
  employees: EmployeeDto[];
}

export interface TeamDto {
  id: number;
  name: string;
  primaryColor: string;
  secondaryColor: string;
  disabled: boolean;
}

export interface EmployeeDto {
  id: number;
  name: string;
  color: string;
  disabled: boolean;
}

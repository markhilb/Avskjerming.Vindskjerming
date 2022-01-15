import { ChangeDetectionStrategy, Component, TemplateRef, ViewChild } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { Store } from '@ngrx/store';
import { EmployeeDto, TeamDto } from 'src/app/models/event.model';
import { AppState, createEmployee, deleteEmployee, getEmployees, selectEmployees, updateEmployee } from 'src/app/store';
import { createTeam, deleteTeam, getTeams, selectTeams, updateTeam } from 'src/app/store/team';

@Component({
  selector: 'app-settings-page',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './settings-page.component.html',
  styleUrls: ['./settings-page.component.scss'],
})
export class SettingsPageComponent {
  @ViewChild('addTeamModal', { static: true }) addTeamModal?: TemplateRef<any>;
  @ViewChild('addEmployeeModal', { static: true }) addEmployeeModal?: TemplateRef<any>;

  modalTeam: TeamDto = {} as TeamDto;
  modalEmployee: EmployeeDto = {} as EmployeeDto;

  teams$ = this.store.select(selectTeams);
  employees$ = this.store.select(selectEmployees);

  constructor(private modal: NgbModal, private store: Store<AppState>) {
    store.dispatch(getTeams());
    store.dispatch(getEmployees());
  }

  addTeam() {
    this.modalTeam = { id: 0, name: '', primaryColor: '#ffffff', secondaryColor: '#bbbbbb' } as TeamDto;
    this.modal.open(this.addTeamModal, { size: 'lg', centered: true });
  }

  confirmAddTeam() {
    this.store.dispatch(createTeam({ team: this.modalTeam }));
    this.modal.dismissAll();
  }

  updateTeam(team: TeamDto) {
    this.modalTeam = { ...team };
    this.modal.open(this.addTeamModal, { size: 'lg', centered: true });
  }

  confirmUpdateTeam() {
    this.store.dispatch(updateTeam({ team: this.modalTeam }));
    this.modal.dismissAll();
  }

  deleteTeam(id: number) {
    this.store.dispatch(deleteTeam({ id }));
  }

  addEmployee() {
    this.modalEmployee = { id: 0, name: '' } as EmployeeDto;
    this.modal.open(this.addEmployeeModal, { size: 'lg', centered: true });
  }

  confirmAddEmployee() {
    this.store.dispatch(createEmployee({ employee: this.modalEmployee }));
    this.modal.dismissAll();
  }

  updateEmployee(employee: EmployeeDto) {
    this.modalEmployee = { ...employee };
    this.modal.open(this.addEmployeeModal, { size: 'lg', centered: true });
  }

  confirmUpdateEmployee() {
    this.store.dispatch(updateEmployee({ employee: this.modalEmployee }));
    this.modal.dismissAll();
  }

  deleteEmployee(id: number) {
    this.store.dispatch(deleteEmployee({ id }));
  }

  save() {}
}

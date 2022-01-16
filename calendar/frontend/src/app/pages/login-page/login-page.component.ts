import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { UntilDestroy, untilDestroyed } from '@ngneat/until-destroy';
import { ofType } from '@ngrx/effects';
import { ActionsSubject, Store } from '@ngrx/store';
import { AppState, login, loginFailed } from 'src/app/store';

@UntilDestroy()
@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss'],
})
export class LoginPageComponent {
  loginFailed = false;

  fg = new FormGroup({
    password: new FormControl('', [Validators.required]),
  });

  constructor(private store: Store<AppState>, actions: ActionsSubject) {
    setTimeout(() => document.getElementById('password')?.focus(), 0);

    actions.pipe(untilDestroyed(this), ofType(loginFailed)).subscribe(() => (this.loginFailed = true));
  }

  login() {
    if (!this.fg.valid) {
      this.fg.markAllAsTouched();
    } else {
      this.store.dispatch(login(this.fg.value));
    }
  }
}

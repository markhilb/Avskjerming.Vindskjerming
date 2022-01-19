import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, exhaustMap, map } from 'rxjs/operators';
import { AuthenticationService } from 'src/app/services/api/authentication.service';
import { ToastService } from 'src/app/services/toast.service';
import * as A from './authentication.actions';

@Injectable()
export class AuthenticationEffects {
  login$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.login),
      exhaustMap((action) =>
        this.authService.login(action.password).pipe(
          map((ok) => {
            if (ok) {
              this.router.navigateByUrl('');
              return A.loginOk();
            }
            return A.loginFailed();
          }),
          catchError((error) => this.toastService.error(error)),
        ),
      ),
    ),
  );

  logout$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.logout),
      exhaustMap(() =>
        this.authService.logout().pipe(
          map(() => A.logoutOk()),
          catchError((error) => this.toastService.error(error)),
        ),
      ),
    ),
  );

  isLoggedIn$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.isLoggedIn),
      exhaustMap(() =>
        this.authService.isLoggedIn().pipe(
          map((isLoggedIn) => A.isLoggedInOk({ isLoggedIn })),
          catchError((error) => this.toastService.error(error)),
        ),
      ),
    ),
  );

  changePassword$ = createEffect(() =>
    this.actions.pipe(
      ofType(A.changePassword),
      exhaustMap((action) =>
        this.authService.changePassword(action.oldPassword, action.newPassword).pipe(
          map((ok) => {
            if (ok) {
              this.toastService.success('Passord endret');
              return A.changePasswordOk();
            }
            return A.changePasswordFailed();
          }),
          catchError((error) => this.toastService.error(error)),
        ),
      ),
    ),
  );

  constructor(
    private actions: Actions,
    private authService: AuthenticationService,
    private toastService: ToastService,
    private router: Router,
  ) {}
}

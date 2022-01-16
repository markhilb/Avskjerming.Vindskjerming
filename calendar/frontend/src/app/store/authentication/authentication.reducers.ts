import { createReducer, on } from '@ngrx/store';
import { initialAuthenticationState, AuthenticationState } from './authentication.state';
import * as A from './authentication.actions';

export const authenticationReducer = createReducer(
  initialAuthenticationState,
  on(
    A.loginOk,
    (state): AuthenticationState => ({
      ...state,
      isLoggedIn: true,
    }),
  ),
  on(
    A.loginFailed,
    A.logoutOk,
    (state): AuthenticationState => ({
      ...state,
      isLoggedIn: false,
    }),
  ),
  on(
    A.isLoggedInOk,
    (state, { isLoggedIn }): AuthenticationState => ({
      ...state,
      isLoggedIn,
    }),
  ),
);

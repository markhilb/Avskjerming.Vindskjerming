import { createAction, props } from '@ngrx/store';

export const login = createAction('[Authentication] Login', props<{ password: string }>());
export const loginOk = createAction('[Authentication] Login Ok');
export const loginFailed = createAction('[Authentication] Login Failed');

export const logout = createAction('[Authentication] Logout');
export const logoutOk = createAction('[Authentication] Logout Ok');

export const isLoggedIn = createAction('[Authentication] Is logged in');
export const isLoggedInOk = createAction('[Authentication] Is logged in Ok', props<{ isLoggedIn: boolean }>());

export const changePassword = createAction(
  '[Authentication] Change password',
  props<{ oldPassword: string; newPassword: string }>(),
);
export const changePasswordOk = createAction('[Authentication] Change password Ok');
export const changePasswordFailed = createAction('[Authentication] Change password Failed');

import { createSelector, select } from '@ngrx/store';
import { filter, OperatorFunction, pipe } from 'rxjs';
import { selectAppState } from '../app.reducers';

export const selectAuthenticationState = createSelector(selectAppState, (state) => state.authenticationState);

export const selectIsLoggedIn = createSelector(selectAuthenticationState, (state) => state.isLoggedIn);

export const selectIsLoggedInDefined = pipe(
  select(selectIsLoggedIn),
  filter((isLoggedIn) => isLoggedIn !== undefined) as OperatorFunction<boolean | undefined, boolean>,
);

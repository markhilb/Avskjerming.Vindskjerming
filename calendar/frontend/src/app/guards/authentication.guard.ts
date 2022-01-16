import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { Observable, map, tap } from 'rxjs';
import { AppState, selectIsLoggedInDefined } from '../store';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationGuard implements CanActivate {
  constructor(private store: Store<AppState>, private router: Router) {}

  canActivate = (): Observable<boolean> =>
    this.store.pipe(
      selectIsLoggedInDefined,
      tap((isLoggedIn) => !isLoggedIn && this.router.navigateByUrl('login')),
    );
}

@Injectable({
  providedIn: 'root',
})
export class AnonymousGuard implements CanActivate {
  constructor(private store: Store<AppState>, private router: Router) {}

  canActivate = (): Observable<boolean> =>
    this.store.pipe(
      selectIsLoggedInDefined,
      tap((isLoggedIn) => isLoggedIn && this.router.navigateByUrl('')),
      map((isLoggedIn) => !isLoggedIn),
    );
}

import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseApiService } from './base-api.service';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  constructor(private api: BaseApiService) {}

  login = (password: string): Observable<boolean> => this.api.post<boolean>('Authentication/Login', { password });

  logout = (): Observable<void> => this.api.post<void>('Authentication/Logout');

  isLoggedIn = (): Observable<boolean> => this.api.get<boolean>('Authentication/IsLoggedIn');

  changePassword = (oldPassword: string, newPassword: string): Observable<boolean> =>
    this.api.post<boolean>('Authentication/changePassword', { oldPassword, newPassword });
}

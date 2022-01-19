import { CommonModule, registerLocaleData } from '@angular/common';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Injectable, LOCALE_ID, NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import {
  CalendarDateFormatter,
  CalendarModule,
  CalendarNativeDateFormatter,
  DateAdapter,
  DateFormatterParams,
} from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CalendarPageComponent } from './pages/calendar-page/calendar-page.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FlatpickrModule } from 'angularx-flatpickr';
import { HttpClientModule } from '@angular/common/http';
import { SettingsPageComponent } from './pages/settings-page/settings-page.component';
import { StoreModule } from '@ngrx/store';
import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { environment } from 'src/environments/environment';
import { EffectsModule } from '@ngrx/effects';
import { appEffects, appReducers } from './store';
import { WeekEventComponent } from './pages/calendar-page/week-event/week-event.component';
import { ToastComponent } from './components/toast/toast.component';
import localeNo from '@angular/common/locales/no';
import { metaReducers } from './store/app.reducers';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { ChangePasswordComponent } from './pages/change-password/change-password.component';

@Injectable()
class CustomDateFormatter extends CalendarNativeDateFormatter {
  override dayViewHour({ date }: DateFormatterParams): string {
    return new Intl.DateTimeFormat('no-NO', {
      hour: 'numeric',
      minute: 'numeric',
    }).format(date);
  }

  override weekViewHour({ date }: DateFormatterParams): string {
    return new Intl.DateTimeFormat('no-NO', {
      hour: 'numeric',
      minute: 'numeric',
    }).format(date);
  }
}

registerLocaleData(localeNo);

@NgModule({
  declarations: [
    AppComponent,
    CalendarPageComponent,
    SettingsPageComponent,
    WeekEventComponent,
    ToastComponent,
    LoginPageComponent,
    ChangePasswordComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    FlatpickrModule.forRoot(),
    CalendarModule.forRoot(
      {
        provide: DateAdapter,
        useFactory: adapterFactory,
      },
      {
        dateFormatter: {
          provide: CalendarDateFormatter,
          useClass: CustomDateFormatter,
        },
      },
    ),
    NgbModule,
    StoreModule.forRoot(appReducers, { metaReducers }),
    EffectsModule.forRoot(appEffects),
    StoreDevtoolsModule.instrument({
      maxAge: 25,
      logOnly: environment.production,
    }),
  ],
  providers: [{ provide: LOCALE_ID, useValue: 'no-NO' }],
  bootstrap: [AppComponent],
})
export class AppModule {}

import { Injectable } from '@angular/core';
import { EMPTY, Subject } from 'rxjs';
import { Toast, ToastType } from 'src/app/models/toast.model';

@Injectable({
  providedIn: 'root',
})
export class ToastService {
  toast$: Subject<Toast> = new Subject<Toast>();

  constructor() {}

  success(message: string) {
    this.toast$.next(new Toast(ToastType.Success, message));
    return EMPTY;
  }

  error(message: string) {
    this.toast$.next(new Toast(ToastType.Error, message));
    return EMPTY;
  }
}

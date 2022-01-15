import { Component } from '@angular/core';
import { UntilDestroy, untilDestroyed } from '@ngneat/until-destroy';
import { Toast } from 'src/app/models/toast.model';
import { ToastService } from 'src/app/services/toast.service';

@UntilDestroy()
@Component({
  selector: 'app-toast',
  templateUrl: './toast.component.html',
  styleUrls: ['./toast.component.scss'],
})
export class ToastComponent {
  toasts: Toast[] = [];

  constructor(toastService: ToastService) {
    toastService.toast$.pipe(untilDestroyed(this)).subscribe((toast) => {
      this.toasts.unshift(toast);
      setTimeout(() => {
        const idx = this.toasts.findIndex((x) => x.id === toast.id);
        idx !== -1 && this.toasts.splice(idx, 1);
      }, 7100);
    });
  }

  onDelete = (idx: number) => this.toasts.splice(idx, 1);
}

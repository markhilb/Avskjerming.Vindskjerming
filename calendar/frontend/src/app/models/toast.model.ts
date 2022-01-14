export class Toast {
  id: number;
  type: ToastType;
  message: string;

  constructor(type: ToastType, message: string) {
    this.id = new Date().getTime();
    this.type = type;
    this.message = message;
  }
}

export enum ToastType {
  Success = 'success',
  Error = 'error',
}

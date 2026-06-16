import { useEffect, useState, type DialogHTMLAttributes } from "react";
import "./Dialog.css";

export function Dialog({
  open,
  ...props
}: DialogHTMLAttributes<HTMLDialogElement>) {
  const [dialog, setDialog] = useState<HTMLDialogElement | null>(null);

  useEffect(() => {
    if (!dialog) {
      return;
    }

    if (open) {
      dialog.showModal();
      dialog.focus();
    } else {
      dialog.close();
    }
  }, [dialog, open]);

  return <dialog ref={setDialog} closedby="any" {...props} />;
}

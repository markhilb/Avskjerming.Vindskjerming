import type { InputHTMLAttributes } from "react";

export interface Props extends Omit<
  InputHTMLAttributes<HTMLInputElement>,
  "onChange"
> {
  inline?: boolean;
  onChange: (value: string | undefined) => void;
}

export function Input({
  title,
  inline,
  style,
  value,
  onChange,
  ...props
}: Props) {
  return (
    <div style={style}>
      {title && (
        <span>
          {title}
          {!inline && <br />}
        </span>
      )}
      <input
        value={value ?? ""}
        onChange={(e) =>
          onChange(e.target.value !== "" ? e.target.value : undefined)
        }
        {...props}
      />
    </div>
  );
}

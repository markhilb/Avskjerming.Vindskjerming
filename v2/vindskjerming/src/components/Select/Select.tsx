import type { HTMLAttributes } from "react";

interface Props<T> extends Omit<HTMLAttributes<HTMLDivElement>, "onChange"> {
  title?: string;
  value: T;
  options: readonly T[];
  onChange: (value: T) => void;
}

export function Select<T extends string>({
  title,
  value,
  options,
  onChange,
  ...props
}: Props<T>) {
  return (
    <div {...props}>
      {title && (
        <span>
          {title}
          <br />
        </span>
      )}
      <select value={value} onChange={(e) => onChange(e.target.value as T)}>
        {options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </div>
  );
}

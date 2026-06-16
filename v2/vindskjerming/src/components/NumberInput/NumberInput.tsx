import Big from "big.js";
import { useState } from "react";
import { Input, type Props as InputProps } from "../Input/Input";

interface Props extends Omit<InputProps, "value" | "onChange"> {
  value: Big | undefined;
  onChange: (value: Big | undefined) => void;
}

export function NumberInput({ value, onChange, ...props }: Props) {
  const fixed = value?.toFixed() ?? "";

  const [prev, setPrev] = useState(fixed);
  const [input, setInput] = useState(fixed);

  if (fixed !== prev) {
    setInput(fixed);
    setPrev(fixed);
  }

  return (
    <Input
      type="number"
      inputMode="decimal"
      value={input}
      onChange={(val) => {
        if (val === undefined) {
          setInput("");
          setPrev("");
          onChange(undefined);
          return;
        }

        try {
          const num = Big(val);
          const fix = num.toFixed();
          setInput(fix);
          setPrev(fix);
          onChange(num);
        } catch {
          setPrev("");
          onChange(undefined);
        }
      }}
      {...props}
    />
  );
}

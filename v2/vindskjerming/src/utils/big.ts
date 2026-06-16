import type Big from "big.js";

export function min(a: Big, b: Big): Big {
  return b.lt(a) ? b : a;
}

export function max(a: Big, b: Big): Big {
  return b.gt(a) ? b : a;
}

import Big from "big.js";
import { GlassType, MountType, Transport, type ItemType } from "../AppState";

export function unreachable(value: never): never {
  throw new Error(`Unreachable code reached, value: ${value}`);
}

function isOneOf<const T extends readonly string[]>(
  value: string,
  values: T,
): value is T[number] {
  return values.includes(value);
}

export function parseArray(value: unknown): unknown[] {
  if (value instanceof Array) {
    return value;
  }
  throw new Error(`Invalid value '${value}', expected Array`);
}

export function parseString(value: unknown): string {
  if (typeof value === "string") {
    return value;
  }
  throw new Error(`Invalid value '${value}', expected string`);
}

export function parseBig(value: unknown): Big {
  if (typeof value === "string" || typeof value === "number") {
    return Big(value);
  }
  throw new Error(`Invalid value '${value}', expected Big`);
}

function parseT<T extends string>(
  value: unknown,
  values: readonly T[],
  decoding: Record<string, T>,
): T {
  const str = parseString(value);
  if (isOneOf(str, values)) {
    return str;
  }

  const decoded = decoding[str];
  if (decoded !== undefined) {
    return decoded;
  }

  throw new Error(
    `Invalid value '${value}', expected one of [${values.join(", ")}]`,
  );
}

export function parseGlassType(value: unknown): GlassType {
  return parseT(value, GlassType, GLASS_TYPE_DECODING);
}

export function parseMountType(value: unknown): MountType {
  return parseT(value, MountType, MOUNT_TYPE_DECODING);
}

export function parseTransport(value: unknown): Transport {
  return parseT(value, Transport, TRANSPORT_DECODING);
}

type Invert<T extends Record<PropertyKey, PropertyKey>> = {
  [K in keyof T as T[K]]: K;
};

function invert<T extends Record<PropertyKey, PropertyKey>>(obj: T): Invert<T> {
  return Object.fromEntries(
    Object.entries(obj).map(([k, v]) => [v, k]),
  ) as Invert<T>;
}

export const ITEM_TYPE_ENCODING = {
  Glass: "glass",
  Stolpe: "post",
  Veggskinne: "wallmount",
} as const satisfies Record<ItemType, string>;

export const ITEM_TYPE_DECODING = invert(ITEM_TYPE_ENCODING);

export const GLASS_TYPE_ENCODING = {
  Klart: "klart",
  Frost: "frost",
} as const satisfies Record<GlassType, string>;

export const GLASS_TYPE_DECODING = invert(GLASS_TYPE_ENCODING);

export const MOUNT_TYPE_ENCODING = {
  Stolpe: "post",
  Veggskinne: "wallmount",
} as const satisfies Record<MountType, string>;

export const MOUNT_TYPE_DECODING = invert(MOUNT_TYPE_ENCODING);

export const TRANSPORT_ENCODING = {
  Sendes: "sendes",
  Hentes: "hentes",
  Monteres: "monteres",
} as const satisfies Record<Transport, string>;

export const TRANSPORT_DECODING = invert(TRANSPORT_ENCODING);

export type PartialPick<T, K extends keyof T> = Omit<T, K> &
  Partial<Pick<T, K>>;

import Big from "big.js";
import type { ItemType } from "./AppState";

export const Config = {
  Veggskinne: {
    lastWidth: Big("0.3"),
    heightMargin: Big("0.5"),
    packagingWeight: Big("50"),
    weightMultiplier: Big("0.1"),
  },
  Stolpe: {
    width: Big("1.3"),
    lastWidth: Big("0.5"),
    heightMargin: Big("0.5"),
    marginPolygon: Big("2"),
    mountWeight: Big("54"),
    packagingWeight: Big("100"),
    weightMultiplier: Big("0.1568"),
  },
  Glass: {
    packagingWeight: Big("200"),
    weightMultiplier: Big("0.618"),
  },
} as const satisfies Record<ItemType, object>;

export type Config = typeof Config;

import Big from "big.js";

export interface GlassItem {
  id: string;
  type: "Glass";
  width: Big;
  height: Big;
  secondHeight: Big;
}

export interface PostItem {
  id: string;
  type: "Stolpe";
  height: Big;
}

export interface WallmountItem {
  id: string;
  type: "Veggskinne";
  height: Big;
}

export type Item = GlassItem | PostItem | WallmountItem;

export type ItemType = Item["type"];

export const MountType = [
  "Stolpe",
  "Veggskinne",
] as const satisfies readonly ItemType[];

export type MountType = (typeof MountType)[number];

export const GlassType = ["Klart", "Frost"] as const;

export type GlassType = (typeof GlassType)[number];

export const Transport = ["Sendes", "Hentes", "Monteres"] as const;

export type Transport = (typeof Transport)[number];

export interface AppState {
  items: { left: Item[]; right: Item[] };
  totalLengthLeft: Big | undefined;
  totalLengthRight: Big | undefined;
  globalWidth: Big | undefined;
  globalHeight: Big | undefined;
  individualWidth: Big | undefined;
  individualHeight: Big | undefined;
  glassSecondHeight: Big | undefined;
  customerName: string | undefined;
  orderNumber: string | undefined;
  glassType: GlassType;
  transport: Transport;
  leftMount: MountType;
  rightMount: MountType;
}

export const initialAppState: AppState = {
  items: { left: [], right: [] },
  totalLengthLeft: undefined,
  totalLengthRight: undefined,
  globalWidth: Big("60"),
  globalHeight: Big("60"),
  individualWidth: Big("60"),
  individualHeight: Big("60"),
  glassSecondHeight: Big("20"),
  customerName: undefined,
  orderNumber: undefined,
  glassType: "Klart",
  transport: "Sendes",
  leftMount: "Veggskinne",
  rightMount: "Stolpe",
};

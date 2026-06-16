import Big from "big.js";
import {
  MountType,
  type GlassItem,
  type Item,
  type PostItem,
  type WallmountItem,
} from "~/AppState";
import { Config } from "~/Config";
import { unreachable, type PartialPick } from "./index";

export function isValid(
  value: Big | undefined,
  min = "10",
  max = "9999",
): value is Big {
  return (
    value !== undefined && value.gt("0") && value.gte(min) && value.lte(max)
  );
}

export function generateItems(
  totalWidth: Big | undefined,
  width: Big | undefined,
  height: Big | undefined,
  leftMount: MountType | undefined,
  rightMount: MountType,
): Item[] {
  const items: Item[] = [];

  if (!isValid(totalWidth) || !isValid(width) || !isValid(height)) {
    return items;
  }

  let curWidth = Big("0");

  if (leftMount) {
    const config = Config[leftMount];
    items.push({
      id: crypto.randomUUID(),
      type: leftMount,
      height: height.add(config.heightMargin),
    });
    curWidth = curWidth.add(config.lastWidth);
  } else {
    // This is the right wall, which means we need to add the width of the end post of the left wall
    curWidth = curWidth.add(Config.Stolpe.lastWidth);
  }

  generateItemsLoop(items, totalWidth, curWidth, width, height, rightMount);

  return items;
}

export type EditItem =
  | PartialPick<GlassItem, "width" | "height" | "secondHeight">
  | PartialPick<PostItem, "height">
  | PartialPick<WallmountItem, "height">;

export function editItem(
  item: EditItem,
  items: Item[],
  totalWidth: Big | undefined,
  globalWidth: Big | undefined,
  globalHeight: Big | undefined,
  rightMount: MountType,
  phantomPost: boolean,
): Item[] | undefined {
  switch (item.type) {
    case "Glass": {
      const { id, type, width, height, secondHeight, ..._rest } = item;

      ({}) satisfies Required<typeof _rest>;

      if (
        !isValid(width, "0") ||
        !isValid(height, "0") ||
        !isValid(secondHeight, "0")
      ) {
        return undefined;
      }

      const idx = items.findIndex((v) => v.id === id);
      const oldItem = items[idx];

      if (oldItem?.type !== type) {
        return undefined;
      }

      const cmp = oldItem.width.cmp(width);
      switch (cmp) {
        // `oldItem.width === width`
        case 0: {
          const newItem = { id, type, width, height, secondHeight };
          return items.map((v) => (v.id === id ? newItem : v));
        }
        // `oldItem.width > width`
        case 1: {
          if (
            !isValid(totalWidth) ||
            !isValid(globalWidth) ||
            !isValid(globalHeight)
          ) {
            return undefined;
          }

          const newItems = items.toSpliced(
            idx,
            items.length - idx,
            { id, type, width, height, secondHeight },
            {
              id: crypto.randomUUID(),
              type: "Stolpe",
              height: height.add(Config.Stolpe.heightMargin),
            },
          );

          generateItemsLoop(
            newItems,
            totalWidth,
            itemsWidth(newItems, phantomPost, false),
            globalWidth,
            globalHeight,
            rightMount,
          );

          return newItems;
        }
        // `oldItem.width < width`
        case -1: {
          // Add back items until `totalWidth` is reached, stopping and cutting when necessary.

          if (
            !isValid(totalWidth) ||
            !isValid(globalWidth) ||
            !isValid(globalHeight)
          ) {
            return undefined;
          }

          const newItems = items.toSpliced(idx);

          const curWidth = itemsWidth(newItems, phantomPost, false);
          const rightMountWidth = Config[rightMount].lastWidth;

          if (curWidth.add(width).add(rightMountWidth).gte(totalWidth)) {
            newItems.push({
              id: crypto.randomUUID(),
              type: "Glass",
              width: totalWidth.sub(curWidth).sub(rightMountWidth),
              height,
              secondHeight: height,
            });
            newItems.push({
              id: crypto.randomUUID(),
              type: rightMount,
              height: height.add(Config[rightMount].heightMargin),
            });
          } else {
            newItems.push({ id, type, width, height, secondHeight });
            newItems.push({
              id: crypto.randomUUID(),
              type: "Stolpe",
              height: globalHeight.add(Config.Stolpe.heightMargin),
            });
            generateItemsLoop(
              newItems,
              totalWidth,
              curWidth.add(width).add(Config.Stolpe.width),
              globalWidth,
              globalHeight,
              rightMount,
            );
          }

          return newItems;
        }
        default:
          return unreachable(cmp);
      }
    }
    case "Stolpe":
    case "Veggskinne": {
      const { id, type, height, ..._rest } = item;

      ({}) satisfies Required<typeof _rest>;

      if (!height || height.lte("0")) {
        return undefined;
      }

      return items.map((v) => (v.id === id ? { id, type, height } : v));
    }
    default:
      unreachable(item);
  }
}

export function itemsWidth(
  items: Item[],
  phantomPost: boolean,
  lastWidth: boolean,
): Big {
  return items
    .reduce((tot, cur, i, arr) => {
      switch (cur.type) {
        case "Glass":
          return tot.add(cur.width);
        case "Stolpe": {
          const cfg = Config[cur.type];
          return tot.add(
            lastWidth && (i === 0 || i === arr.length - 1)
              ? cfg.lastWidth
              : cfg.width,
          );
        }
        case "Veggskinne":
          return tot.add(Config[cur.type].lastWidth);
        default:
          unreachable(cur);
      }
    }, Big("0"))
    .add(phantomPost ? Config.Stolpe.lastWidth : "0");
}

function generateItemsLoop(
  items: Item[],
  totalWidth: Big,
  curWidth: Big,
  width: Big,
  height: Big,
  rightMount: MountType,
) {
  const rightMountWidth = Config[rightMount].lastWidth;

  while (true) {
    const remainder = totalWidth.sub(curWidth).sub(rightMountWidth);

    if (remainder.lte("0")) {
      break;
    } else if (remainder.lte(width)) {
      items.push({
        id: crypto.randomUUID(),
        type: "Glass",
        width: remainder,
        height,
        secondHeight: height,
      });
      items.push({
        id: crypto.randomUUID(),
        type: rightMount,
        height: height.add(Config[rightMount].heightMargin),
      });
      break;
    } else {
      items.push({
        id: crypto.randomUUID(),
        type: "Glass",
        width,
        height,
        secondHeight: height,
      });
      items.push({
        id: crypto.randomUUID(),
        type: "Stolpe",
        height: height.add(Config.Stolpe.heightMargin),
      });
      curWidth = curWidth.add(width).add(Config.Stolpe.width);
    }
  }
}

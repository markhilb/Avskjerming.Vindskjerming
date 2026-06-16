import Big from "big.js";
import { useMemo, type HTMLAttributes } from "react";
import type { GlassType, Item } from "~/AppState";
import { Config } from "~/Config";
import { unreachable } from "~/utils/index";

interface Props extends HTMLAttributes<HTMLTableElement> {
  items: Item[];
  glassType: GlassType;
}

export function PackageList({ items, glassType, ...props }: Props) {
  const [list, weight] = useMemo(() => {
    if (items.length === 0) {
      return [undefined, undefined];
    }

    let weight = Big("0");

    // { [key]: { [size]: count } }
    const map: Record<string, Record<string, number>> = {};

    for (const item of items) {
      let key;
      let size;

      switch (item.type) {
        case "Glass": {
          const config = Config[item.type];

          if (item.height.eq(item.secondHeight)) {
            key = `Glass (${glassType.toLowerCase()})`;
            size = `${item.width.toFixed()}x${item.height.toFixed()}`;
          } else {
            key = `Skrå glass (${glassType.toLowerCase()})`;
            size = `${item.width.toFixed()}x${item.height.toFixed()}x${item.secondHeight.toFixed()}`;
          }

          const area = item.width
            .mul(item.height)
            .sub(item.width.mul(item.height.sub(item.secondHeight)).div("2"));

          weight = weight
            .add(area.mul(config.weightMultiplier))
            .add(config.packagingWeight);

          break;
        }
        case "Stolpe": {
          const config = Config[item.type];

          key = item.type;
          size = item.height.toFixed();

          weight = weight
            .add(item.height.mul(config.weightMultiplier))
            .add(config.mountWeight)
            .add(config.packagingWeight);

          break;
        }
        case "Veggskinne": {
          const config = Config[item.type];

          key = item.type;
          size = item.height.toFixed();

          weight = weight
            .add(item.height.mul(config.weightMultiplier))
            .add(config.packagingWeight);

          break;
        }
        default:
          unreachable(item);
      }

      const sizes = (map[key] ??= {});
      sizes[size] = (sizes[size] ?? 0) + 1;
    }

    const list = [];

    for (const [_key, sizes] of Object.entries(map)) {
      let key = _key;
      for (const [size, count] of Object.entries(sizes)) {
        list.push({ id: `${_key}-${size}`, key, size, count });
        key = "";
      }
    }

    weight = weight.div("1000");

    return [list, weight];
  }, [items, glassType]);

  return (
    <table
      {...props}
      style={{
        minWidth: "20rem",
        border: "solid 1px var(--black)",
        textAlign: "center",
        ...props.style,
      }}
    >
      <thead>
        <tr>
          <th>Type</th>
          <th>Størrelse</th>
          <th>Antall</th>
        </tr>
      </thead>
      <tbody>
        {list?.map(({ id, key, size, count }) => (
          <tr key={id}>
            <td>{key}</td>
            <td>{size}</td>
            <td>{count}</td>
          </tr>
        ))}
        {weight && (
          <tr>
            <td>Vekt</td>
            <td></td>
            <td>{weight.toFixed(0)} kg</td>
          </tr>
        )}
      </tbody>
    </table>
  );
}

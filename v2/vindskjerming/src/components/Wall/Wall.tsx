import Big from "big.js";
import { useMemo, useState, type HTMLAttributes } from "react";
import type { GlassType, Item, MountType, PostItem } from "~/AppState";
import { editItem, itemsWidth, unreachable, type EditItem } from "~/utils";
import { Dialog } from "../Dialog/Dialog";
import { NumberInput } from "../NumberInput/NumberInput";
import "./Wall.css";

interface Props extends Omit<HTMLAttributes<HTMLDivElement>, "onChange"> {
  items: Item[];
  totalWidth: Big | undefined;
  globalWidth: Big | undefined;
  globalHeight: Big | undefined;
  glassType: GlassType;
  rightMount: MountType;
  phantomPost?: PostItem;
  onChange: (items: Item[]) => void;
}

export function Wall({
  items,
  totalWidth,
  globalWidth,
  globalHeight,
  glassType,
  rightMount,
  phantomPost,
  onChange,
  ...props
}: Props) {
  const [selected, setSelected] = useState<EditItem | undefined>(undefined);

  const width = useMemo(
    () => itemsWidth(items, !!phantomPost, true),
    [items, phantomPost],
  );

  if (selected && !items.some((v) => v.id === selected.id)) {
    setSelected(undefined);
  }

  const onClose = () => setSelected(undefined);

  const onDelete = () => {
    if (!selected) {
      return;
    }

    const idx = items.findIndex((v) => v.id === selected.id);
    if (idx >= 0) {
      onChange(items.toSpliced(idx, 2));
      onClose();
    }
  };

  const onSave = () => {
    if (!selected) {
      return;
    }

    const newItems = editItem(
      selected,
      items,
      totalWidth,
      globalWidth,
      globalHeight,
      rightMount,
      !!phantomPost,
    );

    if (newItems) {
      onChange(newItems);
      onClose();
    }
  };

  return (
    <div {...props}>
      <div style={{ display: "flex", alignItems: "end" }}>
        {phantomPost && (
          <div
            className="Stolpe phantom"
            style={{
              height: phantomPost.height.add("5").toFixed() + "px",
            }}
          >
            <div className="post-base" />
          </div>
        )}
        {items.map((item) => (
          <div
            key={item.id}
            className={item.type}
            title={`Rediger ${item.type.toLowerCase()}`}
            style={
              item.type === "Stolpe" || item.type === "Veggskinne"
                ? {
                    height: item.height.add("5").toFixed() + "px",
                  }
                : item.type === "Glass"
                  ? {
                      width: item.width.toFixed() + "px",
                    }
                  : unreachable(item)
            }
            onClick={() => setSelected(item)}
          >
            {item.type === "Glass" && (
              <>
                <p>
                  {item.width.toFixed()}x{item.height.toFixed()}
                  {!item.height.eq(item.secondHeight) && (
                    <>x{item.secondHeight.toFixed()}</>
                  )}
                </p>
                <div
                  style={{
                    borderLeftWidth:
                      item.width.round(0, Big.roundUp).toFixed() + "px",
                    borderLeftColor: GLASS_COLOR[glassType],
                    borderTopWidth:
                      (item.height.gt(item.secondHeight)
                        ? item.height.sub(item.secondHeight)
                        : item.secondHeight.sub(item.height)
                      ).toFixed() + "px",
                    height:
                      (item.height.gt(item.secondHeight)
                        ? item.secondHeight
                        : item.height
                      ).toFixed() + "px",
                  }}
                />
              </>
            )}
            {item.type === "Stolpe" && <div className="post-base" />}
          </div>
        ))}
      </div>

      {items.length > 0 && (
        <div>
          <div className="length-bar">
            <div className="end left"></div>
            <div className="end right"></div>
          </div>
          <p style={{ textAlign: "center" }}>{width.toFixed()}</p>
        </div>
      )}

      {selected && (
        <Dialog open style={{ gap: "2rem" }} onClose={onClose}>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "auto auto",
              alignItems: "center",
              gap: "1rem",
            }}
          >
            <span style={{ gridRow: 2, gridColumn: 1 }}>Høyde:</span>
            <NumberInput
              style={{ gridRow: 2, gridColumn: 2 }}
              value={selected.height}
              onChange={(height) => setSelected({ ...selected, height })}
            />
            {selected.type === "Glass" && (
              <>
                <span style={{ gridRow: 1, gridColumn: 1 }}>Bredde:</span>
                <NumberInput
                  style={{ gridRow: 1, gridColumn: 2 }}
                  value={selected.width}
                  onChange={(width) => setSelected({ ...selected, width })}
                />
                <span style={{ gridRow: 3, gridColumn: 1 }}>Skrå høyde:</span>
                <NumberInput
                  style={{ gridRow: 3, gridColumn: 2 }}
                  value={selected.secondHeight}
                  onChange={(secondHeight) =>
                    setSelected({ ...selected, secondHeight })
                  }
                />
              </>
            )}
          </div>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              borderTop: "1px solid gray",
              paddingTop: "1rem",
            }}
          >
            <button onClick={onClose}>Avbryt</button>
            <button onClick={onDelete}>Slett</button>
            <button onClick={onSave}>Lagre</button>
          </div>
        </Dialog>
      )}
    </div>
  );
}

const GLASS_COLOR: Record<GlassType, string> = { Klart: "blue", Frost: "red" };

import { useMemo, useState } from "react";
import "./App.css";
import { AppStateContext } from "./AppContext";
import {
  GlassType,
  initialAppState,
  MountType,
  Transport,
  type AppState,
} from "./AppState";
import {
  Header,
  Input,
  NumberInput,
  PackageList,
  Select,
  Wall,
} from "./components";
import { Config } from "./Config";
import { generateItems as _generateItems, isValid, itemsWidth } from "./utils";
import { min } from "./utils/big";

function App() {
  const [state, setState] = useState<AppState>(initialAppState);

  const {
    items,
    totalLengthLeft,
    totalLengthRight,
    globalWidth,
    globalHeight,
    individualWidth,
    individualHeight,
    glassSecondHeight,
    customerName,
    orderNumber,
    glassType,
    transport,
    leftMount,
    rightMount,
  } = state;

  const update = (value: Partial<AppState>) =>
    setState((v) => ({ ...v, ...value }));

  const generateItems = (value: Partial<AppState>): AppState["items"] => {
    const get = <K extends keyof AppState>(key: K): AppState[K] | undefined =>
      key in value ? value[key] : state[key];

    const right = _generateItems(
      get("totalLengthRight"),
      get("globalWidth"),
      get("globalHeight"),
      undefined,
      value.rightMount ?? rightMount,
    );

    const left = _generateItems(
      get("totalLengthLeft"),
      get("globalWidth"),
      get("globalHeight"),
      get("leftMount"),
      right.length > 0 ? "Stolpe" : (value.rightMount ?? rightMount),
    );

    return { left, right };
  };

  const onAddMount = (mountType: MountType) => {
    if (!isValid(individualHeight)) {
      return;
    }

    const config = Config[mountType];

    const addMount = (side: keyof typeof items, totalLength: Big): boolean => {
      const itms = items[side];
      const last = itms[itms.length - 1];

      if (last?.type === "Glass") {
        const curWidth = itemsWidth(itms, side === "right", false);
        const remainder = totalLength.sub(curWidth).sub(config.lastWidth);

        if (remainder.gte("0")) {
          update({
            items: {
              ...items,
              [side]: itms.concat({
                id: crypto.randomUUID(),
                type: mountType,
                height: individualHeight.add(config.heightMargin),
              }),
            },
          });
          return true;
        }

        const newWidth = last.width.add(remainder);
        if (newWidth.gt("0")) {
          update({
            items: {
              ...items,
              [side]: itms.toSpliced(
                itms.length - 1,
                1,
                {
                  ...last,
                  width: newWidth,
                },
                {
                  id: crypto.randomUUID(),
                  type: mountType,
                  height: individualHeight.add(config.heightMargin),
                },
              ),
            },
          });
          return true;
        }
      }

      return false;
    };

    if (isValid(totalLengthLeft)) {
      if (items.left.length === 0) {
        // Items is empty, add mount
        update({
          items: {
            ...items,
            left: [
              {
                id: crypto.randomUUID(),
                type: mountType,
                height: individualHeight.add(config.heightMargin),
              },
            ],
          },
        });
        return;
      }
      if (addMount("left", totalLengthLeft)) {
        return;
      }
    }

    if (isValid(totalLengthRight)) {
      addMount("right", totalLengthRight);
    }
  };

  const onAddGlass = () => {
    if (!isValid(individualWidth) || !isValid(individualHeight)) {
      return;
    }

    const addGlass = (side: keyof typeof items, totalLength: Big): boolean => {
      const itms = items[side];
      const last = itms[itms.length - 1];

      if (
        last &&
        (last.type === "Stolpe" ||
          (last.type === "Veggskinne" && itms.length === 1))
      ) {
        const curWidth = itemsWidth(itms, side === "right", false);
        if (totalLength.gt(curWidth)) {
          update({
            items: {
              ...items,
              [side]: itms.concat({
                id: crypto.randomUUID(),
                type: "Glass",
                width: min(individualWidth, totalLength.sub(curWidth)),
                height: individualHeight,
                secondHeight: individualHeight,
              }),
            },
          });
          return true;
        }
      }

      return false;
    };

    if (isValid(totalLengthLeft)) {
      if (addGlass("left", totalLengthLeft)) {
        return;
      }
    }

    if (isValid(totalLengthRight)) {
      addGlass("right", totalLengthRight);
    }
  };

  const allItems = useMemo(() => items.left.concat(items.right), [items]);

  const last = items.left[items.left.length - 1];
  const phantomPost = last?.type === "Stolpe" ? last : undefined;

  return (
    <AppStateContext value={{ state, onChange: setState }}>
      <Header state={state} onChange={setState} />

      <div
        style={{
          display: "grid",
          gridTemplateRows:
            "min-content min-content min-content auto min-content min-content",
          gap: "1rem",
          marginInline: "1rem",
          marginBottom: "1rem",
          flexGrow: 1,
        }}
      >
        <h2 className="no-print" style={{ textAlign: "center" }}>
          Automatisk utregning
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr auto 1fr",
            gap: "1rem",
          }}
        >
          <div style={{ display: "flex", gap: "1rem", gridColumn: 2 }}>
            <NumberInput
              title="Total lengde venstre:"
              value={totalLengthLeft}
              onChange={(totalLengthLeft) =>
                update({
                  totalLengthLeft,
                  items: generateItems({ totalLengthLeft }),
                })
              }
            />
            <NumberInput
              title="Total lengde høyre:"
              value={totalLengthRight}
              onChange={(totalLengthRight) =>
                update({
                  totalLengthRight,
                  items: generateItems({ totalLengthRight }),
                })
              }
            />
          </div>
          <div
            style={{
              display: "flex",
              gap: "1rem",
              gridColumn: 3,
              justifySelf: "end",
            }}
          >
            <Input
              title="Kundenavn:"
              value={customerName}
              onChange={(customerName) => update({ customerName })}
            />
            <Input
              title="Ordrenummer:"
              value={orderNumber}
              onChange={(orderNumber) => update({ orderNumber })}
            />
          </div>
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr auto 1fr",
            gap: "1rem",
          }}
        >
          <div style={{ display: "flex", gap: "1rem" }}>
            <Select
              className="no-print"
              title="Glass type:"
              value={glassType}
              options={GlassType}
              onChange={(glassType) => update({ glassType })}
            />
            <Select
              title="Transport:"
              value={transport}
              options={Transport}
              onChange={(transport) => update({ transport })}
            />
          </div>

          <div
            className="no-print"
            style={{ display: "flex", gap: "1rem", alignSelf: "start" }}
          >
            <Select
              value={leftMount}
              options={MountType}
              style={{ alignSelf: "end" }}
              onChange={(leftMount) =>
                update({ leftMount, items: generateItems({ leftMount }) })
              }
            />
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "auto auto",
                alignItems: "center",
                columnGap: "0.5rem",
              }}
            >
              <span style={{ gridRow: 1, gridColumn: 1 }}>Global bredde:</span>
              <NumberInput
                style={{ gridRow: 1, gridColumn: 2 }}
                value={globalWidth}
                onChange={(globalWidth) =>
                  update({ globalWidth, items: generateItems({ globalWidth }) })
                }
              />
              <span style={{ gridRow: 2, gridColumn: 1 }}>Global høyde:</span>
              <NumberInput
                style={{ gridRow: 2, gridColumn: 2 }}
                value={globalHeight}
                onChange={(globalHeight) =>
                  update({
                    globalHeight,
                    items: generateItems({ globalHeight }),
                  })
                }
              />
            </div>
            <Select
              value={rightMount}
              options={MountType}
              style={{ alignSelf: "end" }}
              onChange={(rightMount) =>
                update({ rightMount, items: generateItems({ rightMount }) })
              }
            />
          </div>

          <PackageList
            items={allItems}
            glassType={glassType}
            style={{ gridColumn: 3, justifySelf: "end" }}
          />
        </div>

        <div style={{ display: "flex", overflowX: "auto" }}>
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              rowGap: "1rem",
              columnGap: "4rem",
              justifyContent: "center",
              margin: "auto",
            }}
          >
            {items.left.length > 0 && (
              <Wall
                items={items.left}
                totalWidth={totalLengthLeft}
                globalWidth={globalWidth}
                globalHeight={globalHeight}
                glassType={glassType}
                rightMount={items.right.length > 0 ? "Stolpe" : rightMount}
                onChange={(left) => update({ items: { ...items, left } })}
              />
            )}
            {items.right.length > 0 && (
              <Wall
                items={items.right}
                totalWidth={totalLengthRight}
                globalWidth={globalWidth}
                globalHeight={globalHeight}
                glassType={glassType}
                rightMount={rightMount}
                phantomPost={phantomPost}
                onChange={(right) => update({ items: { ...items, right } })}
              />
            )}
          </div>
        </div>

        <h2 className="no-print" style={{ textAlign: "center" }}>
          Manuel utregning
        </h2>

        <div
          className="no-print"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr auto 1fr",
            columnGap: "1rem",
          }}
        >
          <div
            style={{
              display: "flex",
              justifySelf: "end",
              alignSelf: "center",
              gap: "0.5rem",
            }}
          >
            <button onClick={() => onAddMount("Veggskinne")}>Veggskinne</button>
            <button onClick={() => onAddMount("Stolpe")}>Stolpe</button>
            <button onClick={onAddGlass}>Glass</button>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "auto auto",
              alignItems: "center",
              columnGap: "0.5rem",
            }}
          >
            <span style={{ gridRow: 1, gridColumn: 1 }}>
              Individuell bredde:
            </span>
            <NumberInput
              style={{ gridRow: 1, gridColumn: 2 }}
              value={individualWidth}
              onChange={(individualWidth) => update({ individualWidth })}
            />
            <span style={{ gridRow: 2, gridColumn: 1 }}>
              Individuell høyde:
            </span>
            <NumberInput
              style={{ gridRow: 2, gridColumn: 2 }}
              value={individualHeight}
              onChange={(individualHeight) => update({ individualHeight })}
            />
          </div>

          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifySelf: "end",
              gap: "0.5rem",
            }}
          >
            <button onClick={() => {}}>Skrå glass</button>
            <NumberInput
              value={glassSecondHeight}
              onChange={(glassSecondHeight) => update({ glassSecondHeight })}
            />
          </div>
        </div>
      </div>
    </AppStateContext>
  );
}

export default App;

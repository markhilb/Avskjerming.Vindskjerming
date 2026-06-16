import Big from "big.js";
import { useRef } from "react";
import type { AppState, Item } from "~/AppState";
import {
  GLASS_TYPE_ENCODING,
  MOUNT_TYPE_ENCODING,
  parseArray,
  parseBig,
  parseGlassType,
  parseMountType,
  parseString,
  parseTransport,
  TRANSPORT_ENCODING,
  unreachable,
} from "~/utils/index";
import "./Header.css";

interface Props {
  state: AppState;
  onChange: (state: AppState) => void;
}

export function Header({ state, onChange }: Props) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const onSave = () => {
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
      ..._rest
    } = state;

    ({}) satisfies Required<typeof _rest>;

    const encodeItem = (item: Item) => {
      switch (item.type) {
        case "Glass":
          return [
            "Glass",
            `${item.width.toFixed()}x${item.height.toFixed()}x${item.secondHeight.toFixed()}`,
          ];
        case "Stolpe":
          return ["Post", item.height.toFixed()];
        case "Veggskinne":
          return ["Wallmount", item.height.toFixed()];
        default:
          unreachable(item);
      }
    };

    const url = URL.createObjectURL(
      new Blob(
        [
          JSON.stringify({
            _totalWidthL: totalLengthLeft?.toFixed(),
            _totalWidthR: totalLengthRight?.toFixed(),
            _globalWidth: globalWidth?.toFixed(),
            _globalHeight: globalHeight?.toFixed(),
            _glassType: GLASS_TYPE_ENCODING[glassType],
            _leftMount: MOUNT_TYPE_ENCODING[leftMount],
            _rightMount: MOUNT_TYPE_ENCODING[rightMount],
            customer: customerName,
            orderNumber: orderNumber,
            individualWidth: individualWidth?.toFixed(),
            individualHeight: individualHeight?.toFixed(),
            secondGlassHeight: glassSecondHeight?.toFixed(),
            transport: TRANSPORT_ENCODING[transport],
            items: [items.left.map(encodeItem), items.right.map(encodeItem)],
          }),
        ],
        { type: "text/plain;charset=utf-8" },
      ),
    );

    const a = document.createElement("a");
    a.href = url;
    a.download = state.orderNumber ?? "vindskjerming";
    a.click();

    setTimeout(() => URL.revokeObjectURL(url));
  };

  const onLoad = () => fileInputRef.current?.click();

  const handleLoad = (data: string) => {
    const decodeItem = (value: unknown): Item => {
      const [_type, size] = parseArray(value);
      const type = parseString(_type);

      switch (type) {
        case "Glass": {
          const [width, height, secondHeight] = parseString(size).split("x");
          return {
            id: crypto.randomUUID(),
            type: "Glass",
            width: Big(width ?? "error"),
            height: Big(height ?? "error"),
            secondHeight: Big(secondHeight ?? "error"),
          };
        }
        case "Post":
          return {
            id: crypto.randomUUID(),
            type: "Stolpe",
            height: parseBig(size),
          };
        case "Wallmount":
          return {
            id: crypto.randomUUID(),
            type: "Veggskinne",
            height: parseBig(size),
          };
      }

      throw new Error(`Invalid value '${value}', expected Item`);
    };

    try {
      const json = JSON.parse(data);

      const [_left, _right] = parseArray(json.items);
      const left = parseArray(_left);
      const right = parseArray(_right);

      const newState = {
        totalLengthLeft: parseBig(json._totalWidthL),
        totalLengthRight: parseBig(json._totalWidthR),
        globalWidth: parseBig(json._globalWidth),
        globalHeight: parseBig(json._globalHeight),
        glassType: parseGlassType(json._glassType),
        leftMount: parseMountType(json._leftMount),
        rightMount: parseMountType(json._rightMount),
        customerName: parseString(json.customer),
        orderNumber: parseString(json.orderNumber),
        individualWidth: parseBig(json.individualWidth),
        individualHeight: parseBig(json.individualHeight),
        glassSecondHeight: parseBig(json.secondGlassHeight),
        transport: parseTransport(json.transport),
        items: {
          left: left.map(decodeItem),
          right: right.map(decodeItem),
        },
      };

      onChange(newState);
    } catch (e) {
      console.log("Decode error:", e);
    }
  };

  const onReset = () => onChange({ ...state, items: { left: [], right: [] } });

  const onUndo = () =>
    onChange({
      ...state,
      items: {
        left:
          state.items.right.length > 0
            ? state.items.left
            : state.items.left.slice(0, -1),
        right: state.items.right.slice(0, -1),
      },
    });

  return (
    <>
      <div className="header no-print">
        <button onClick={onSave}>Lagre</button>
        <button onClick={onLoad}>Last opp</button>
        <button onClick={window.print}>Eksporter</button>
        <hr />
        <button onClick={onReset}>Reset</button>
        <button onClick={onUndo}>Angre</button>
      </div>

      <div className="logo print">
        <img src="/avskjerming-logo.png" />
        <h2>Vindskjerming</h2>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept=".txt"
        style={{ display: "none" }}
        onChange={(e) => {
          const files = e.target.files;
          if (files?.[0]) {
            const reader = new FileReader();

            reader.onload = () => {
              if (typeof reader.result === "string") {
                handleLoad(reader.result);
              }
              e.target.value = "";
            };

            reader.readAsText(files[0]);
          }
        }}
      />
    </>
  );
}

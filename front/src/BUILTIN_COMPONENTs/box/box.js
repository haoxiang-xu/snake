import React, { useEffect, useState, useContext } from "react";
import { MatrixParameterContext } from "../matrix/matrixParameterContexts";
import { symbolManifest } from "./symbol_manifest";

const Box = ({ position, code }) => {
  const { matrixSize, boxSize, CTTmappingTable } = useContext(
    MatrixParameterContext
  );
  const [boxPosition, setBoxPosition] = useState({ x: 0, y: 0 });

  const [symbol, setSymbol] = useState(symbolManifest["empty_box"]);
  const [symbolTransform, setSymbolTransform] = useState("rotate(0deg)");
  const [isSymbolLoaded, setIsSymbolLoaded] = useState(false);

  useEffect(() => {
    if (position && position.x !== undefined && position.y !== undefined) {
      setBoxPosition(position);
    }
  }, []);
  useEffect(() => {
    const set_symbol_transform = async (type, code) => {
      if (type === "snake_head") {
        if (code === 2) {
          setSymbolTransform("rotate(270deg)");
        } else if (code === 3) {
          setSymbolTransform("rotate(0deg)");
        } else if (code === 4) {
          setSymbolTransform("rotate(90deg)");
        } else if (code === 5) {
          setSymbolTransform("rotate(180deg)");
        }
      } else if (type === "snake_tail") {
        if (code === 12) {
          setSymbolTransform("rotate(270deg)");
        } else if (code === 13) {
          setSymbolTransform("rotate(0deg)");
        } else if (code === 14) {
          setSymbolTransform("rotate(90deg)");
        } else if (code === 15) {
          setSymbolTransform("rotate(180deg)");
        }
      } else if (type === "snake_body") {
        if (code === 6) {
          setSymbolTransform("rotate(90deg)");
        } else if (code === 7) {
          setSymbolTransform("rotate(0deg)");
        }
      } else if (type === "snake_turn") {
        if (code === 8) {
          setSymbolTransform("rotate(0deg)");
        } else if (code === 9) {
          setSymbolTransform("rotate(270deg)");
        } else if (code === 10) {
          setSymbolTransform("rotate(180deg)");
        } else if (code === 11) {
          setSymbolTransform("rotate(90deg)");
        }
      }
    };
    const conver_code_to_type = async () => {
      return new Promise((resolve, reject) => {
        if (CTTmappingTable[code]) {
          resolve(CTTmappingTable[code]);
        } else {
          reject("Invalid code");
        }
      });
    };
    const fetch_symbol = async () => {
      try {
        const type = await conver_code_to_type();
        const svg = await symbolManifest[type]();
        await set_symbol_transform(type, code);
        setSymbol(svg.default);
        setIsSymbolLoaded(true);
      } catch (e) {
        console.log(e);
      }
    };
    fetch_symbol();
  }, [code]);

  if (!isSymbolLoaded) return null;
  return (
    <div
      style={{
        position: "absolute",
        transform: symbolTransform,

        top: `${boxPosition.y * boxSize.height}px`,
        left: `${boxPosition.x * boxSize.width}px`,

        width: `${boxSize.width}px`,
        height: `${boxSize.height}px`,

        userSelect: "none",
        pointerEvents: "none",
      }}
    >
      <img
        src={symbol}
        style={{
          width: `${boxSize.width}px`,
          height: `${boxSize.height}px`,
        }}
      />
    </div>
  );
};

export default Box;

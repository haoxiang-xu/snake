import React, { useEffect, useRef, useState } from "react";
import { MatrixParameterContext } from "./matrixParameterContexts";
import Box from "../box/box";
import Snake from "../snake/snake";

const default_matrix_size = { height: 10, width: 10 };
const default_box_size = { height: 32, width: 32 };

const FAKE_MATRIX = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 16, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
];
const FAKE_SNAKE = [
  [3, 0],
  [2, 0],
  [2, 1],
  [2, 2],
  [2, 3],
  [2, 4],
  [2, 5],
  [2, 6],
  [2, 7],
  [2, 8],
  [2, 9],
  [3, 9],
  [4, 9],
  [5, 9],
  [6, 9],
  [7, 9],
  [8, 9],
  [9, 9],
  [9, 8],
  [9, 7],
  [9, 6],
  [9, 5],
  [9, 4],
  [9, 3],
  [9, 2],
  [9, 1],
  [9, 0],
  [8, 0],
  [7, 0],

];

const Matrix = ({ size, box_size }) => {
  /* Matrix parameters ----------------------------------------------------- */
  const [matrixSize, setMatrixSize] = useState(default_matrix_size);
  const [boxSize, setBoxSize] = useState(default_box_size);
  useEffect(() => {
    if (size && size.height && size.width) {
      setMatrixSize(size);
    } else {
      setMatrixSize(default_matrix_size);
    }
    if (box_size && box_size.height && box_size.width) {
      setBoxSize(box_size);
    } else {
      setBoxSize(default_box_size);
    }
  }, []);
  /* { code to type mapping table } */
  const [CTTmappingTable, setCTTMappingTable] = useState({});
  const [TTCmappingTable, setTTCMappingTable] = useState({});
  useEffect(() => {
    const mappingTable = {
      0: "invisible",
      1: "empty_box",

      2: "snake_head",
      3: "snake_head",
      4: "snake_head",
      5: "snake_head",

      6: "snake_body",
      7: "snake_body",

      8: "snake_turn",
      9: "snake_turn",
      10: "snake_turn",
      11: "snake_turn",

      12: "snake_tail",
      13: "snake_tail",
      14: "snake_tail",
      15: "snake_tail",

      16: "candy_box",
    };
    const reverseMappingTable = {
      invisible: 0,
      empty_box: 1,

      snake_head_top: 2,
      snake_head_right: 3,
      snake_head_bottom: 4,
      snake_head_left: 5,

      snake_body_vertical: 6,
      snake_body_horizontal: 7,

      snake_turn_top_right: 8,
      snake_turn_right_bottom: 9,
      snake_turn_bottom_left: 10,
      snake_turn_left_top: 11,

      snake_tail_top: 12,
      snake_tail_right: 13,
      snake_tail_bottom: 14,
      snake_tail_left: 15,

      candy_box: 16,
    };
    setCTTMappingTable(mappingTable);
    setTTCMappingTable(reverseMappingTable);
  }, [matrixSize]);
  /* Matrix parameters ----------------------------------------------------- */

  /* Board ----------------------------------------------------------------- */
  const [board, setBoard] = useState(FAKE_MATRIX);
  const [renderedBoard, setRenderedBoard] = useState([]);
  useEffect(() => {
    const boxes = [];
    for (let i = 0; i < matrixSize.height; i++) {
      for (let j = 0; j < matrixSize.width; j++) {
        boxes.push(
          <Box
            key={`board-${i}-${j}`}
            position={{ x: j, y: i }}
            code={board[i][j]}
          />
        );
      }
    }
    setRenderedBoard(boxes);
  }, [matrixSize, boxSize, board]);
  /* Board ----------------------------------------------------------------- */

  /* Snake ----------------------------------------------------------------- */
  const [snakeSequence, setSnakeSequence] = useState(FAKE_SNAKE);

  return (
    <MatrixParameterContext.Provider
      value={{ matrixSize, boxSize, CTTmappingTable, TTCmappingTable }}
    >
      <div
        style={{
          position: "absolute",

          top: "50%",
          left: "50%",

          height: matrixSize.height * boxSize.height,
          width: matrixSize.width * boxSize.width,

          transform: "translate(-50%, -50%)",
        }}
      >
        {renderedBoard}
        <Snake snake_sequence={snakeSequence} />
      </div>
    </MatrixParameterContext.Provider>
  );
};

export default Matrix;

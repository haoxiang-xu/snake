import React, { useEffect, useRef, useState, useContext } from "react";
import { MatrixParameterContext } from "../matrix/matrixParameterContexts";
import Box from "../box/box";

const Snake = ({ snake_sequence }) => {
  const { TTCmappingTable } = useContext(MatrixParameterContext);

  const [snakeSequence, setSnakeSequence] = useState([]);
  const [renderedSnake, setRenderedSnake] = useState([]);
  useEffect(() => {
    if (snake_sequence) {
      setSnakeSequence(snake_sequence);
    }
  }, []);

  useEffect(() => {
    const push_snake_head = (i) => {
      const head = snakeSequence[i];
      const next = snakeSequence[i + 1];

      if (head[0] === next[0] && head[1] === next[1] + 1) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_head_bottom"]}
          />
        );
      } else if (head[0] === next[0] + 1 && head[1] === next[1]) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_head_right"]}
          />
        );
      } else if (head[0] === next[0] && head[1] === next[1] - 1) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_head_top"]}
          />
        );
      } else if (head[0] === next[0] - 1 && head[1] === next[1]) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_head_left"]}
          />
        );
      }
    };
    const push_snake_tail = (i) => {
      const tail = snakeSequence[i];
      const prev = snakeSequence[i - 1];

      if (tail[0] === prev[0] && tail[1] === prev[1] + 1) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_tail_bottom"]}
          />
        );
      } else if (tail[0] === prev[0] + 1 && tail[1] === prev[1]) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_tail_right"]}
          />
        );
      } else if (tail[0] === prev[0] && tail[1] === prev[1] - 1) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_tail_top"]}
          />
        );
      } else if (tail[0] === prev[0] - 1 && tail[1] === prev[1]) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_tail_left"]}
          />
        );
      }
    };
    const push_snake_body = (i) => {
      const body = snakeSequence[i];
      const prev = snakeSequence[i - 1];
      const next = snakeSequence[i + 1];

      if (prev[0] === next[0] && prev[0] === body[0]) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_body_vertical"]}
          />
        );
      } else if (prev[1] === next[1] && prev[1] === body[1]) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_body_horizontal"]}
          />
        );
      } else if (prev[0] === body[0] && prev[1] === body[1] + 1) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_turn_top_right"]}
          />
        );
      } else if (prev[1] === body[1] && prev[0] === body[0] + 1) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_turn_right_bottom"]}
          />
        );
      } else if (prev[0] === body[0] && prev[1] === body[1] - 1) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_turn_bottom_left"]}
          />
        );
      } else if (prev[1] === body[1] && prev[0] === body[0] - 1) {
        return (
          <Box
            key={`snake-${i}`}
            position={{ x: snakeSequence[i][0], y: snakeSequence[i][1] }}
            code={TTCmappingTable["snake_turn_left_top"]}
          />
        );
      }
    };
    const snake = [];
    for (let i = 0; i < snakeSequence.length; i++) {
      if (i === 0) {
        snake.push(push_snake_head(i));
      } else if (i === snakeSequence.length - 1) {
        snake.push(push_snake_tail(i));
      } else {
        snake.push(push_snake_body(i));
      }
    }
    setRenderedSnake(snake);
  }, [snakeSequence]);

  return <>{renderedSnake}</>;
};

export default Snake;

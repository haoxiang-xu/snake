import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Main from "./PAGEs/main";

const App = () => {
  return (
    <div
      className="App"
      style={{
        position: "absolute",
        top: "50%",
        left: "50%",
        height: "100vh",
        width: "100vw",
        transform: "translate(-50%, -50%)",
        overflow: "hidden",
      }}
    >
      <Router>
        <Routes>
          <Route path="/" element={<Main />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App;

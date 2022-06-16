import "./App.scss";
import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Map from "../pages/Map";
import Form from "../pages/Form";
import About from "../pages/About";
import Downloads from "../pages/Downloads";

import Header from "../components/Header";

function App() {
  return (
    <div className="app container">
      <Header />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/map" element={<Map />} />
        <Route path="/form" element={<Form />} />
        <Route path="/about" element={<About />} />
        <Route path="/download" element={<Downloads />} />
      </Routes>
    </div>
  );
}

export default App;

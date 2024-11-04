import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Scans from "./pages/Scans";
import Files from "./pages/Files";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-base-200">
        <Navbar />
        <main className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/scans" element={<Scans />} />
            <Route path="/files" element={<Files />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

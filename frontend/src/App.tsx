import "./index.css";
import Header from "./components/Header.tsx";
import Dashboard from "./components/Dashboard.tsx";
import Projects from "./components/Projects.tsx";
import { HashRouter , Route, Routes } from "react-router-dom";

function App() {
  return (
    <>
      <HashRouter>
        <div className="min-h-full">
          <Header />
          <main>
            <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/projects" element={<Projects />} />
              </Routes>
            </div>
          </main>
        </div>
      </HashRouter>
    </>
  );
}

export default App;

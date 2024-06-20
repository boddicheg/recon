import "./index.css";
import Header from "./components/HeaderComponent";
import Dashboard from "./components/DashboardComponent";
import Projects from "./components/ProjectsComponent";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

function App() {
  return (
    <>
      <Router>
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
      </Router>
    </>
  );
}

export default App;

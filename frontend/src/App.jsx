import Navbar from "./components/Navbar";
import CompareSection from "./components/CompareSection";

function App() {
  return (
    <div className="min-h-screen bg-white dark:bg-slate-950 text-black dark:text-white transition-all">
      <Navbar />
      <div className="max-w-6xl mx-auto px-6 py-10">
        <CompareSection />
      </div>
    </div>
  );
}

export default App;
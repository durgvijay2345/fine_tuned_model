import { useTheme } from "../ThemeContext";
import { Sun, Moon } from "lucide-react";

export default function Navbar() {
  const { dark, setDark } = useTheme();

  return (
    <nav className="flex justify-between items-center px-10 py-5 border-b dark:border-white/10">
      <div>
        <h1 className="text-2xl font-bold text-indigo-500">
          PlagiarismAI
        </h1>
        <p className="text-xs text-gray-400">
          AI Semantic Similarity Engine
        </p>
      </div>

      <button
        onClick={() => setDark(!dark)}
        className="p-2 rounded-lg bg-slate-200 dark:bg-slate-800"
      >
        {dark ? <Sun size={18} /> : <Moon size={18} />}
      </button>
    </nav>
  );
}
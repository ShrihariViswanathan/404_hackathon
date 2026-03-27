import { motion } from "framer-motion";

export default function LearnPage({ onNext }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      className="text-center backdrop-blur-xl bg-white/5 border border-white/10 p-10 rounded-3xl"
    >
      {/* 🔥 Hook Line */}
      <h2 className="text-red-400 text-sm mb-4 tracking-widest">
        90% OF TRADERS FAIL
      </h2>

      {/* 💣 Main Headline */}
      <h1 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight">
        Can you
        <span className="block bg-gradient-to-r from-cyan-400 to-purple-500 text-transparent bg-clip-text">
          survive the market?
        </span>
      </h1>

      {/* 🧠 Subtext */}
      <p className="text-gray-400 mb-10 text-lg">
        TradeCraft isn’t a course.  
        It’s a survival game.
      </p>

      {/* 🚀 CTA */}
      <motion.button
        whileHover={{ scale: 1.08 }}
        whileTap={{ scale: 0.95 }}
        onClick={onNext}
        className="px-10 py-4 rounded-2xl bg-gradient-to-r from-cyan-400 to-purple-500 text-black font-bold text-lg shadow-lg"
      >
        Enter the Arena →
      </motion.button>

      {/* 👇 subtle curiosity trigger */}
      <p className="text-xs text-gray-500 mt-6">
        No experience needed. No mercy given.
      </p>
    </motion.div>
  );
}
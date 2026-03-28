import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useUser, SignInButton } from "@clerk/clerk-react";

const lines = [
  "Initializing TradeCraft...",
  "Connecting to Market...",
  "Analyzing Risk Profile...",
  "Checking Survival Probability...",
  "> Most traders fail.",
  "> You are not ready.",
];

export default function Landing({ onNext }) {
  const [displayedLines, setDisplayedLines] = useState([]);
  const [showFinal, setShowFinal] = useState(false);
  const { isSignedIn } = useUser()

  useEffect(() => {
    let i = 0;

    const interval = setInterval(() => {
      setDisplayedLines((prev) => [...prev, lines[i]]);
      i++;

      if (i === lines.length) {
        clearInterval(interval);
        setTimeout(() => setShowFinal(true), 1200);
      }
    }, 700);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full flex flex-col items-center">

      {/* 🔥 BRAND HEADER (KILLER PART) */}
      <motion.div
        initial={{ opacity: 0, y: -40 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-10 text-center"
      >
        {/* LOGO */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: [0, 1.1, 1] }}
          transition={{ duration: 0.6 }}
          className="flex justify-center mb-6"
        >
          <div className="relative">

            {/* 🔥 Outer Glow Pulse */}
            <motion.div
              animate={{ scale: [1, 1.4, 1], opacity: [0.4, 0.1, 0.4] }}
              transition={{ duration: 2.5, repeat: Infinity }}
              className="absolute inset-0 rounded-[30px] bg-cyan-400/30 blur-2xl"
            />

            {/* 💎 Logo Box */}
            <div className="relative w-24 h-24 rounded-[28px] bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 flex items-center justify-center shadow-lg overflow-hidden">

              {/* 📈 Graph Line */}
              <svg
                viewBox="0 0 100 100"
                className="absolute w-full h-full opacity-20"
              >
                <polyline
                  points="0,70 20,60 40,80 60,40 80,50 100,20"
                  fill="none"
                  stroke="black"
                  strokeWidth="3"
                />
              </svg>

              {/* ⚡ Center Symbol */}
              <span className="text-2xl font-bold text-black">
                ₿
              </span>
            </div>
          </div>
        </motion.div>

        {/* NAME */}
        <h1 className="text-6xl font-black tracking-tight">
          <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-500 text-transparent bg-clip-text">
            TradeCraft
          </span>
        </h1>

        {/* TAGLINE */}
        <p className="text-gray-500 text-sm mt-2 tracking-widest">
          MARKET SIMULATION PROTOCOL
        </p>
      </motion.div>

      {/* 💻 YOUR TERMINAL (UNCHANGED) */}
      <div className="font-mono text-green-400 text-left max-w-2xl w-full">

        <div className="bg-black border border-green-500/30 p-6 rounded-xl shadow-[0_0_40px_rgba(34,197,94,0.2)]">

          {displayedLines.map((line, index) => (
            <motion.p
              key={index}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mb-2"
            >
              {line}
            </motion.p>
          ))}

          {!showFinal && <span className="animate-pulse">█</span>}

          {showFinal && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="mt-8 text-center"
            >
              <h1 className="text-3xl md:text-4xl text-white mb-6">
                Do you still want to enter?
              </h1>

              {/* 🔐 If NOT logged in */}
              {!isSignedIn ? (
                <SignInButton mode="modal">
                  <button className="px-8 py-3 border border-white hover:bg-white hover:text-black transition rounded-lg">
                    ENTER THE MARKET →
                  </button>
                </SignInButton>
              ) : (
                /* ✅ If logged in */
                <button
                  onClick={onNext}
                  className="px-8 py-3 border border-white hover:bg-white hover:text-black transition rounded-lg"
                >
                  ENTER THE MARKET →
                </button>
              )}
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
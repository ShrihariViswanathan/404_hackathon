import { motion } from "framer-motion";
import { useState } from "react";

export default function Question({ setStep, setQuestions }) {

  const handleclick = async () => {
  try {
    const res1 = await fetch('http://127.0.1:8000/placement/refresh/');
    const res = await fetch('http://127.0.0.1:8000/placement/quiz/'); // better endpoint
    const data = await res.json();

    setQuestions(data.questions); // IMPORTANT
    setStep("test");
  } catch (err) {
    console.error("Error fetching questions:", err);
  }
};

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      className="backdrop-blur-xl bg-white/5 border border-white/10 p-8 rounded-3xl text-center glow"
    >
      <h2 className="text-3xl mb-8 font-semibold">
        Do you know trading?
      </h2>

      <div className="space-y-4">
        <button
          value="startQuiz"         
          onClick={handleclick}
          className="w-full py-4 rounded-xl bg-gradient-to-r from-green-400 to-emerald-500 text-black font-semibold hover:scale-105 transition"
        >
          Yes, I have experience
        </button>

        <button
          onClick={() => setStep("learn")}
          className="w-full py-4 rounded-xl bg-gray-800 hover:bg-gray-700 transition"
        >
          No, I'm new
        </button>
      </div>
    </motion.div>
  );
}
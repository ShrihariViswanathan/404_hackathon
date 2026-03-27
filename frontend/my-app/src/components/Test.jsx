import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

export default function Test({ questions }) {
  const navigate = useNavigate();
  const [qIndex, setQIndex] = useState(0);
  const [score, setScore] = useState(0);

  if (!questions || questions.length === 0) {
    return <div className="text-white">Loading questions...</div>;
  }

  const getPoints = (question) => {
  if (question.difficulty === "easy") return 1;
  if (question.difficulty === "medium") return 2;
  if (question.difficulty === "hard") return 3;
  return 1;
};

  const handleAnswer = (i) => {
  let newScore = score;

  if (i === questions[qIndex].answer) {
    newScore += getPoints(questions[qIndex]);
  }

  setScore(newScore);

  if (qIndex + 1 < questions.length) {
    setQIndex(qIndex + 1);
  } else {
    finish(newScore);
  }
};

  const finish = (finalScore) => {
  const maxScore = questions.reduce(
    (sum, q) => sum + getPoints(q),
    0
  );

  const percentage = (finalScore / maxScore) * 100;

  let league = "Bronze";

  if (percentage >= 75) league = "Gold";
  else if (percentage >= 40) league = "Silver";

  localStorage.setItem("league", league);
  localStorage.setItem("score", finalScore);

  navigate("/trade");
};

  return (
    <motion.div className="backdrop-blur-xl bg-white/5 border border-white/10 p-8 rounded-3xl glow">

      {/* Progress Bar */}
      <div className="w-full bg-gray-800 h-2 rounded-full mb-6">
        <div
          className="h-2 bg-cyan-400 rounded-full transition-all"
          style={{ width: `${((qIndex + 1) / questions.length) * 100}%` }}
        />
      </div>

      {/* Question */}
      <h2 className="text-xl mb-6">
        {questions[qIndex].question}
      </h2>

      {/* Options */}
      <div className="space-y-3">
        {questions[qIndex].options.map((opt, i) => (
          <button
            key={i}
            onClick={() => handleAnswer(i)}
            className="w-full py-3 rounded-xl bg-gray-800 hover:bg-cyan-500/20 transition border border-white/10"
          >
            {opt}
          </button>
        ))}
      </div>
    </motion.div>
  );
}
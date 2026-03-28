import { motion } from "framer-motion";
import { useState } from "react";

export default function LearnPage() {
  const [started, setStarted] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState(null);

  const userId = "user_3BY6Wb35eFWrcrohYhOKFCHTjlI"; // ✅ correct
  const unitId = "1";

  const league = "Bronze";

  const startQuiz = async () => {
    setStarted(true);

    // ✅ FIXED URL + HEADER
    const res = await fetch(
      `http://localhost:8000/api/quiz/${unitId}`,
      {
        headers: {
          "x-user-id": userId
        },
        cache: "no-store"
      }
    );

    const data = await res.json();

    console.log("🔥 DATA:", data); // debug

    setQuestions(data.questions || []);
  };

  if (!started) {
    return (
      <motion.div className="text-center p-10 text-white">
        <h1 className="text-5xl font-bold mb-6">Enter Arena</h1>
        <button
          onClick={startQuiz}
          className="bg-cyan-500 px-6 py-3 rounded-xl text-black font-bold"
        >
          Start
        </button>
      </motion.div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="text-white text-center mt-20">
        ❌ No questions (check console)
      </div>
    );
  }

  const q = questions[current];

  const correctIndex =
    typeof q.correct_index === "number"
      ? q.correct_index
      : q.options.indexOf(q.correct_index);

  function handleAnswer(i) {
  setSelected(i);

  const isCorrect = i === correctIndex;

  fetch("http://localhost:8000/api/quiz/record", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-user-id": "user_3BY6Wb35eFWrcrohYhOKFCHTjlI"  // 🔥 FORCE THIS
    },
    body: JSON.stringify({
      question_id: q.id,
      is_correct: isCorrect
    })
  })
    .then(res => res.json())
    .then(data => console.log("🔥 RECORD RESPONSE:", data))
    .catch(err => console.error("❌ RECORD ERROR:", err));
}

  function next() {
    setSelected(null);
    setCurrent((prev) => Math.min(prev + 1, questions.length - 1));
  }

  function prev() {
    setSelected(null);
    setCurrent((prev) => Math.max(prev - 1, 0));
  }

  function retry() {
    setSelected(null);
  }

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center">

      {/* LEAGUE */}
      <div className="w-full max-w-xl mt-6 mb-4 flex justify-between px-4">
        <div className="flex gap-3 items-center">
          <div className="bg-yellow-600 w-10 h-10 rounded-full flex items-center justify-center">
            🥉
          </div>
          <div>
            <p className="text-sm text-gray-400">League</p>
            <p className="font-bold">{league}</p>
          </div>
        </div>

        <div className="text-sm text-gray-400">
          {current + 1} / {questions.length}
        </div>
      </div>

      {/* QUESTION */}
      <div className="max-w-xl w-full bg-zinc-900 p-6 rounded-2xl">
        <h1 className="text-xl mb-6">{q.question_text}</h1>

        <div className="space-y-3">
          {q.options.map((opt, i) => {
            let style = "bg-gray-800";

            if (selected !== null) {
              if (i === correctIndex) style = "bg-green-500";
              else if (i === selected) style = "bg-red-500";
            }

            return (
              <button
                key={i}
                onClick={() => handleAnswer(i)}
                className={`w-full p-3 rounded ${style}`}
              >
                {opt}
              </button>
            );
          })}
        </div>

        {selected !== null && (
          <p className="mt-4">
            {selected === correctIndex ? "✔ Correct" : "✖ Try again"}
          </p>
        )}

        <div className="flex gap-3 mt-6">
          <button onClick={prev} className="bg-gray-700 px-4 py-2 rounded">
            Prev
          </button>

          <button onClick={retry} className="bg-yellow-500 px-4 py-2 rounded text-black">
            Retry
          </button>

          <button onClick={next} className="bg-cyan-500 px-4 py-2 rounded text-black">
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
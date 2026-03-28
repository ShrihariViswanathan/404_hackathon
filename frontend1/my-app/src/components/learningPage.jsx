import { motion } from "framer-motion";
import { useState } from "react";
import { useUser } from "@clerk/clerk-react";

export default function LearnPage() {
  const { user } = useUser();

  const [started, setStarted] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState(null);

  const unitId = "1";

  const startQuiz = async () => {
    setStarted(true);

    const res = await fetch(
      `http://localhost:8000/api/quiz/${unitId}`,
      {
        headers: {
          "x-user-id": user?.id   // 🔥 Clerk ID
        }
      }
    );

    const data = await res.json();
    setQuestions(data.questions || []);
  };

  if (!started) {
    return (
      <div className="text-center p-10 text-white">
        <button onClick={startQuiz}>Start</button>
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
        "x-user-id": user?.id   // 🔥 IMPORTANT
      },
      body: JSON.stringify({
        question_id: q.id,
        is_correct: isCorrect
      })
    });
  }

  return (
    <div className="text-white p-10">
      <h1>{q?.question_text}</h1>

      {q?.options?.map((opt, i) => (
        <button key={i} onClick={() => handleAnswer(i)}>
          {opt}
        </button>
      ))}
    </div>
  );
}
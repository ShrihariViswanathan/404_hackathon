import { useState } from "react";

export default function LearnPage() {
  const [step, setStep] = useState(0);
  const [result, setResult] = useState("");

  const lessons = [
    {
      title: "What is Trading?",
      content: "Trading = Buying low, selling high. Profit comes from price movement.",
    },
    {
      title: "Market Basics",
      content: "Price moves because of demand & supply. More buyers = price goes up.",
    },
    {
      title: "Your First Decision",
      content: "Price is going UP fast. What will you do?",
      action: true,
    },
  ];

  const handleChoice = (choice) => {
    if (choice === "buy") {
      setResult("✅ Good! You followed the trend.");
    } else {
      setResult("❌ Missed opportunity! Market was going up.");
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-10 flex flex-col items-center justify-center">

      <div className="max-w-xl w-full bg-zinc-900 p-6 rounded-2xl shadow-xl">

        <h1 className="text-2xl font-bold mb-4 text-cyan-400">
          {lessons[step].title}
        </h1>

        <p className="text-gray-300 mb-6">
          {lessons[step].content}
        </p>

        {/* INTERACTIVE PART */}
        {lessons[step].action && !result && (
          <div className="flex gap-4">
            <button
              onClick={() => handleChoice("buy")}
              className="flex-1 bg-green-500 py-2 rounded-lg"
            >
              Buy
            </button>
            <button
              onClick={() => handleChoice("sell")}
              className="flex-1 bg-red-500 py-2 rounded-lg"
            >
              Sell
            </button>
          </div>
        )}

        {/* RESULT */}
        {result && (
          <p className="mt-4 font-bold">{result}</p>
        )}

        {/* NEXT BUTTON */}
        <button
          onClick={() => {
            setResult("");
            setStep((prev) => Math.min(prev + 1, lessons.length - 1));
          }}
          className="mt-6 w-full bg-cyan-500 py-2 rounded-lg"
        >
          Next →
        </button>

      </div>
    </div>
  );
}
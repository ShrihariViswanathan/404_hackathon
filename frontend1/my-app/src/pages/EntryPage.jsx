import { useState } from "react";
import Landing from "../components/Landing";
import Question from "../components/Question";
import Test from "../components/Test";
import LearningRedirect from "../components/LearningRedirect";

export default function EntryPage() {
  const [step, setStep] = useState("landing");
 const [questions, setQuestions] = useState([]); // ✅ ADD THIS
  return (
    <div className="h-screen w-screen bg-[#0b0f1a] text-white flex items-center justify-center relative overflow-hidden">

      {/* 🌈 Soft Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute w-[600px] h-[600px] bg-blue-500/20 blur-[150px] rounded-full top-[-200px] left-[-200px]" />
        <div className="absolute w-[500px] h-[500px] bg-purple-500/20 blur-[150px] rounded-full bottom-[-200px] right-[-200px]" />
      </div>

      {/* 💎 Main Content */}
      <div className="z-10 w-full max-w-md px-6">
        {step === "landing" && <Landing onNext={() => setStep("question")} />}
        {step === "question" && <Question setStep={setStep} setQuestions={setQuestions} />}
        {step === "test" &&  <Test questions={questions} />}
        {step === "learn" && <LearningRedirect />}
      </div>
    </div>
  );
  
}
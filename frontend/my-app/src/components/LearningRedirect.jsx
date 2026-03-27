import { useNavigate } from "react-router-dom";


export default function LearningRedirect() {
  const navigate=useNavigate()
  const handleclick=()=>{
    navigate("./learn")
  }
  return (
    <div className="text-center backdrop-blur-xl bg-white/5 border border-white/10 p-10 rounded-3xl glow">
      <h2 className="text-4xl mb-4 font-bold">Welcome Beginner 👋</h2>

      <p className="text-gray-400 mb-8">
        We'll turn you into a trader.
      </p>

      <button onClick={handleclick} className="px-8 py-4 rounded-xl bg-gradient-to-r from-green-400 to-blue-500 text-black font-semibold hover:scale-105 transition">
        Start Learning →
      </button>
    </div>
  );
}
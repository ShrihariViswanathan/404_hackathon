import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function TradePage() {
    const [show, setShow] = useState(false);
    const league = localStorage.getItem("league") || "Bronze";

    const navigate = useNavigate()

    useEffect(() => {
        setTimeout(() => setShow(true), 300);
    }, []);

    const leagueConfig = {
        Bronze: {
            img: "bronze.png",
            glow: "shadow-orange-600/60",
        },
        Silver: {
            img: "silver.png",
            glow: "shadow-gray-400/60",
        },
        Gold: {
            img: "gold.png",
            glow: "shadow-yellow-400/70",
        },
    };

    const config = leagueConfig[league] || leagueConfig["Bronze"];

    return (
        <div className="min-h-screen flex items-center justify-center bg-black relative overflow-hidden text-white">

            {/* FLASH */}
            {show && (
                <motion.div
                    initial={{ opacity: 1 }}
                    animate={{ opacity: 0 }}
                    transition={{ duration: 0.5 }}
                    className="absolute w-full h-full bg-white z-10"
                />
            )}

            {/* GLOW */}
            <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1.5 }}
                transition={{ duration: 1 }}
                className="absolute w-[500px] h-[500px] bg-cyan-500/20 blur-3xl rounded-full"
            />

            {/* BADGE */}
            {show && (
                <motion.div
                    initial={{ scale: 0, rotate: -30, opacity: 0 }}
                    animate={{ scale: 1, rotate: 0, opacity: 1 }}
                    transition={{ type: "spring", stiffness: 120 }}
                    className={`relative z-20 p-6 rounded-full ${config.glow} shadow-2xl`}
                >
                    <motion.img
                        src={config.img}
                        alt={league}
                        className="w-52 h-52"
                        animate={{ scale: [1, 1.1, 1] }}
                        transition={{ duration: 2, repeat: Infinity }}
                    />
                </motion.div>
            )}

            {/* TEXT */}
            {show && (
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="absolute bottom-32 text-center"
                >
                    <h1 className="text-4xl font-bold tracking-widest">
                        {league}
                    </h1>
                    <p className="text-gray-400 mt-2">Rank Unlocked</p>
                </motion.div>
            )}

            {/* CTA */}
            {show && (
                <button
                    onClick={() => navigate("/bitcoin")}
                    style={{
                        position: "absolute",
                        bottom: "50px",
                        padding: "10px 20px",
                        backgroundColor: "cyan",
                        color: "black",
                        border: "none",
                        borderRadius: "8px",
                        cursor: "pointer",
                        zIndex: 50,
                    }}
                >
                    Enter Bitcoin Market →
                </button>
            )}
            
            {show && (
                <button
                    onClick={() => navigate("/stock")}
                    style={{
                        position: "absolute",
                        bottom: "100px",
                        padding: "10px 20px",
                        backgroundColor: "cyan",
                        color: "black",
                        border: "none",
                        borderRadius: "8px",
                        cursor: "pointer",
                        zIndex: 50,
                    }}
                >
                    Enter Stock Market →
                </button>
            )}

        </div>
    );
}
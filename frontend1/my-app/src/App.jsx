import { Routes, Route } from "react-router-dom";
import EntryPage from "./pages/EntryPage";
import LearnPage from "./pages/LearnPage";
import Layout from "./components/element";
import BitcoinPage from "./pages/BitcoinPage";
import StockMarketPage from "./pages/StockMarketPage";

export default function App() {
  return (
    <div className="bg-black min-h-screen font-sans text-white">
      <Routes>
        <Route element={<Layout />}>
        <Route path="/" element={<EntryPage />} />
        <Route path="/trade" element={<TradePage />} />
        <Route path="/learn" element={<LearnPage />} />
        <Route path="/bitcoin" element={<BitcoinPage/>}/>
        <Route path="/stock" element={<StockMarketPage/>}/>
        </Route>
      </Routes>
    </div>
  );
}
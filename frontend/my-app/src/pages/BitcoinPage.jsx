import { useEffect, useRef, useState } from "react";
import { createChart } from "lightweight-charts";

export default function BitcoinPage() {
  const chartRef = useRef();
  const candleSeriesRef = useRef();
  const socketRef = useRef();

  const [symbol, setSymbol] = useState("BINANCE:BTCUSDT");

  const initialBalance = 70000;
  const [balance, setBalance] = useState(initialBalance);
  const [holding, setHolding] = useState(0);
  const [price, setPrice] = useState(0);
  const [qty, setQty] = useState(0.01);

  const [trades, setTrades] = useState([]);

  const candleRef = useRef(null);
  const lastCandleTimeRef = useRef(0);

  // 📊 CHART
  useEffect(() => {
    const chart = createChart(chartRef.current, {
      width: 900,
      height: 450,
      layout: {
        background: { color: "#0b0e11" },
        textColor: "#d1d4dc",
      },
      grid: {
        vertLines: { color: "#1e2329" },
        horzLines: { color: "#1e2329" },
      },
    });

    const candleSeries = chart.addCandlestickSeries({
      upColor: "#0ecb81",
      downColor: "#f6465d",
      borderVisible: false,
    });

    candleSeriesRef.current = candleSeries;

    return () => chart.remove();
  }, []);

  // 🔌 SOCKET
  useEffect(() => {
    const API_KEY = "d737ldhr01qjjol21nk0d737ldhr01qjjol21nkg";

    if (socketRef.current) socketRef.current.close();

    candleRef.current = null;
    lastCandleTimeRef.current = 0;

    const socket = new WebSocket(`wss://ws.finnhub.io?token=${API_KEY}`);
    socketRef.current = socket;

    socket.onopen = () => {
      socket.send(JSON.stringify({ type: "subscribe", symbol }));
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (!data.data) return;

      const trade = data.data[0];
      const newPrice = trade.p;

      setPrice(newPrice);

      const time = Math.floor(Date.now() / 1000);
      const candleTime = Math.floor(time / 5) * 5;

      if (!candleRef.current || candleTime !== lastCandleTimeRef.current) {
        candleRef.current = {
          time: candleTime,
          open: newPrice,
          high: newPrice,
          low: newPrice,
          close: newPrice,
        };
        lastCandleTimeRef.current = candleTime;
      } else {
        candleRef.current.high = Math.max(candleRef.current.high, newPrice);
        candleRef.current.low = Math.min(candleRef.current.low, newPrice);
        candleRef.current.close = newPrice;
      }

      candleSeriesRef.current.update(candleRef.current);
    };

    return () => socket.close();
  }, [symbol]);

  // 💰 CALCULATIONS
  const holdingsValue = holding * price;
  const netWorth = balance + holdingsValue;
  const pnl = netWorth - initialBalance;

  // 🟢 BUY
  const buy = () => {
    if (balance >= price * qty) {
      setHolding((p) => p + qty);
      setBalance((p) => p - price * qty);

      setTrades((prev) => [
        { type: "BUY", price, qty, time: new Date().toLocaleTimeString() },
        ...prev,
      ].slice(0, 30));
    }
  };

  // 🔴 SELL
  const sell = () => {
    if (holding >= qty) {
      setHolding((p) => p - qty);
      setBalance((p) => p + price * qty);

      setTrades((prev) => [
        { type: "SELL", price, qty, time: new Date().toLocaleTimeString() },
        ...prev,
      ].slice(0, 30));
    }
  };

  return (
    <div style={{ background: "#0b0e11", color: "white", minHeight: "100vh", padding: "10px" }}>

      <h2>Live Crypto Charts</h2>

      {/* TOP BAR */}
      <div style={{ marginBottom: "10px", display: "flex", alignItems: "center", gap: "15px" }}>

        <select
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          style={{
            background: "#161b22",
            color: "#c9d1d9",
            border: "1px solid #2a2f36",
            padding: "8px 12px",
            borderRadius: "6px",
            outline: "none",
            cursor: "pointer"
          }}
        >
          <option value="BINANCE:BTCUSDT">BTC</option>
          <option value="BINANCE:ETHUSDT">ETH</option>
          <option value="BINANCE:SOLUSDT">SOL</option>
        </select>

        <span style={{ color: "#c9d1d9" }}>
          Price: ${price ? price.toFixed(2) : "0.00"}
        </span>

      </div>

      {/* MAIN GRID */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "3fr 1.2fr",
        gap: "12px"
      }}>

        {/* CHART */}
        <div>
          <div ref={chartRef}></div>
        </div>

        {/* RIGHT PANEL */}
        <div style={{ background: "#11161c", padding: "15px", borderRadius: "12px" }}>

          <h4 style={{ opacity: 0.6 }}>PORTFOLIO</h4>

          <h2>${netWorth.toFixed(2)}</h2>

          <div style={{
            color: pnl >= 0 ? "#0ecb81" : "#f6465d",
            fontWeight: "bold",
            marginBottom: "10px"
          }}>
            {pnl >= 0 ? "▲" : "▼"} ${Math.abs(pnl).toFixed(2)}
          </div>

          <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
            <div style={{ flex: 1, background: "#161b22", padding: "10px", borderRadius: "10px" }}>
              <div>CASH</div>
              <div>${balance.toFixed(2)}</div>
            </div>

            <div style={{ flex: 1, background: "#161b22", padding: "10px", borderRadius: "10px" }}>
              <div>HOLDING</div>
              <div>{holding.toFixed(4)}</div>
            </div>
          </div>

          <h4>ORDER</h4>

          <div style={{ display: "flex", marginBottom: "10px" }}>
            <button onClick={buy} style={{ flex: 1, padding: "10px", background: "#0ecb81", border: "none" }}>
              Buy
            </button>
            <button onClick={sell} style={{ flex: 1, padding: "10px", background: "#f6465d", border: "none" }}>
              Sell
            </button>
          </div>

          <input
            type="number"
            value={qty}
            min={0.0}
            max={10}
            step={0.1}
            onChange={(e) => setQty(Number(e.target.value))}
            placeholder="0.0000"
            style={{
              width: "100%",
              padding: "10px",
              marginBottom: "10px",
              background: "#161b22",
              border: "1px solid #2a2f36",
              borderRadius: "6px",
              color: "#c9d1d9",
              fontSize: "14px",
              outline: "none"
            }}
            onFocus={(e) => {
              e.target.style.border = "1px solid #0ecb81";
            }}
            onBlur={(e) => {
              e.target.style.border = "1px solid #2a2f36";
            }}
          />

          <div>
            <div>Price: ${price.toFixed(2)}</div>
            <div>Qty: {qty}</div>
            <div>Total: ${(qty * price).toFixed(2)}</div>
          </div>
        </div>
      </div>

      {/* TRADE HISTORY */}
      <div style={{
        background: "#11161c",
        padding: "15px",
        borderRadius: "12px",
        marginTop: "12px"
      }}>
        <h4 style={{ opacity: 0.6 }}>TRADE HISTORY</h4>

        <div style={{ maxHeight: "250px", overflowY: "auto" }}>
          {trades.map((t, i) => (
            <div key={i} style={{
              display: "flex",
              justifyContent: "space-between",
              padding: "6px 0",
              borderBottom: "1px solid #222",
              alignItems:"center",
              width:"100%"
            }}>
              <span style={{
                color: t.type === "BUY" ? "#0ecb81" : "#f6465d",
                fontWeight: "bold"
              }}>
                {t.type}
              </span>

              <span>{t.qty}</span>
              <span>${t.price.toFixed(2)}</span>
              <span style={{ opacity: 0.6 }}>{t.time}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
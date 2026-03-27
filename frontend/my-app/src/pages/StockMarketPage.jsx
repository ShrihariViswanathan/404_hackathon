import { useEffect, useRef, useState } from "react";
import { createChart } from "lightweight-charts";

export default function StockMarketPage() {
  const chartRef = useRef();
  const candleSeriesRef = useRef();

  const candleRef = useRef(null);
  const lastCandleTimeRef = useRef(0);

  const [symbol, setSymbol] = useState("TSLA");

  const initialBalance = 60000;
  const [balance, setBalance] = useState(initialBalance);
  const [holding, setHolding] = useState(0);
  const [price, setPrice] = useState(0);
  const [qty, setQty] = useState(0.1);

  const [trades, setTrades] = useState([]);

  // 📊 CHART
  useEffect(() => {
    candleRef.current = null;
    lastCandleTimeRef.current = 0;
    const API_KEY = "d737gjpr01qn7f07sgigd737gjpr01qn7f07sgj0";

    const chart = createChart(chartRef.current, {
      width: chartRef.current.clientWidth,
      height: chartRef.current.clientHeight,
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
      wickUpColor: "#0ecb81",
      wickDownColor: "#f6465d",
    });

    candleSeries.setData([]);
    candleSeriesRef.current = candleSeries;

    const handleResize = () => {
      chart.applyOptions({
        width: chartRef.current.clientWidth,
        height: chartRef.current.clientHeight,
      });
    };

    window.addEventListener("resize", handleResize);

    let interval;

    const fetchPrice = async () => {
      try {
        const res = await fetch(
          `https://finnhub.io/api/v1/quote?symbol=${symbol}&token=${API_KEY}`
        );
        const data = await res.json();

        const currentPrice = data.c;
        if (!currentPrice) return;

        setPrice(currentPrice);

        const time = Math.floor(Date.now() / 1000);
        const candleTime = Math.floor(time / 5) * 5;

        if (!candleRef.current || candleTime !== lastCandleTimeRef.current) {
          candleRef.current = {
            time: candleTime,
            open: currentPrice,
            high: currentPrice,
            low: currentPrice,
            close: currentPrice,
          };
          lastCandleTimeRef.current = candleTime;
        } else {
          candleRef.current.high = Math.max(candleRef.current.high, currentPrice);
          candleRef.current.low = Math.min(candleRef.current.low, currentPrice);
          candleRef.current.close = currentPrice;
        }

        candleSeriesRef.current.update(candleRef.current);
      } catch (err) {
        console.error(err);
      }
    };

    fetchPrice();
    interval = setInterval(fetchPrice, 3000);

    return () => {
      window.removeEventListener("resize", handleResize);
      clearInterval(interval);
      chart.remove();
    };
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
    <div style={{
      background: "#0b0e11",
      color: "white",
      height: "100vh",
      display: "flex",
      flexDirection: "column"
    }}>

      {/* HEADER */}
      <div style={{
        padding: "12px 20px",
        display: "flex",
        justifyContent: "space-between",
        borderBottom: "1px solid #1e2329"
      }}>
        <h2>{symbol} Dashboard</h2>
        <span>{new Date().toLocaleTimeString()}</span>
      </div>

      {/* SYMBOLS */}
      <div style={{
        padding: "10px 20px",
        display: "flex",
        gap: "10px",
        borderBottom: "1px solid #1e2329"
      }}>
        {["TSLA", "AAPL", "GOOGL", "MSFT"].map((s) => (
          <button
            key={s}
            onClick={() => setSymbol(s)}
            style={{
              padding: "6px 12px",
              background: symbol === s ? "#2962FF" : "#161b22",
              color: symbol === s ? "white" : "#c9d1d9",
              border: "1px solid #2a2f36",
              borderRadius: "8px",
              cursor: "pointer"
            }}
          >
            {s}
          </button>
        ))}
      </div>

      {/* MAIN */}
      <div style={{
        flex: 1,
        display: "grid",
        gridTemplateColumns: "1fr 340px",
        gap: "16px",
        padding: "16px"
      }}>

        {/* CHART CARD */}
        <div style={{
          background: "#11161c",
          borderRadius: "16px",
          padding: "10px",
          boxShadow: "0 0 0 1px #1e2329"
        }}>
          <div
            ref={chartRef}
            style={{
              width: "100%",
              height: "100%",
              borderRadius: "12px",
              overflow: "hidden"
            }}
          />
        </div>

        {/* RIGHT PANEL */}
        <div style={{
          background: "#11161c",
          padding: "20px",
          borderRadius: "16px",
          boxShadow: "0 0 0 1px #1e2329",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between"
        }}>
          <div>
            <h4 style={{ opacity: 0.6 }}>PORTFOLIO</h4>

            <h2>${netWorth.toFixed(2)}</h2>

            <div style={{
              color: pnl >= 0 ? "#0ecb81" : "#f6465d",
              marginBottom: "10px"
            }}>
              {pnl >= 0 ? "▲" : "▼"} ${Math.abs(pnl).toFixed(2)}
            </div>

            {/* CASH / HOLDING */}
            <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
              <div style={{
                flex: 1,
                background: "#161b22",
                padding: "12px",
                borderRadius: "12px",
                textAlign: "center"
              }}>
                <div style={{ opacity: 0.6 }}>CASH</div>
                <div>${balance.toFixed(2)}</div>
              </div>

              <div style={{
                flex: 1,
                background: "#161b22",
                padding: "12px",
                borderRadius: "12px",
                textAlign: "center"
              }}>
                <div style={{ opacity: 0.6 }}>HOLDING</div>
                <div>{holding}</div>
              </div>
            </div>

            <h4>ORDER</h4>

            {/* BUY SELL */}
            <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
              <button onClick={buy} style={{
                flex: 1,
                padding: "12px",
                background: "#0ecb81",
                border: "none",
                borderRadius: "10px",
                fontWeight: "bold"
              }}>
                Buy
              </button>

              <button onClick={sell} style={{
                flex: 1,
                padding: "12px",
                background: "#f6465d",
                border: "none",
                borderRadius: "10px",
                fontWeight: "bold"
              }}>
                Sell
              </button>
            </div>

            <input
              type="number"
              value={qty}
              min={0.1}
              max={11}
              step={0.1}
              defaultValue={0.1}
              onChange={(e) => setQty(Number(e.target.value))}
              style={{
                width: "100%",
                padding: "10px",
                marginBottom: "10px",
                background: "#161b22",
                border: "1px solid #2a2f36",
                borderRadius: "10px",
                color: "white"
              }}
            />

            <div>Price: ${price.toFixed(2)}</div>
            <div>Qty: {qty}</div>
            <div>Total: ${(qty * price).toFixed(2)}</div>
          </div>
        </div>
      </div>

      {/* TRADE HISTORY */}
      <div style={{
        margin: "16px",
        background: "#11161c",
        borderRadius: "16px",
        padding: "15px",
        boxShadow: "0 0 0 1px #1e2329"
      }}>
        <h4 style={{ opacity: 0.6 }}>TRADE HISTORY</h4>

        <div style={{ maxHeight: "200px", overflowY: "auto" }}>
          {trades.map((t, i) => (
            <div key={i} style={{
              display: "flex",
              justifyContent: "space-between",
              padding: "6px 0",
              borderBottom: "1px solid #1e2329",
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

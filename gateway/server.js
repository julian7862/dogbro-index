// -----------------------------------------------------------
// WebSocket Hub - 純粹的 Socket.IO 事件中繼伺服器
// -----------------------------------------------------------
const express = require("express");

const app = express();
const PORT = process.env.PORT || 3001;

/* =========================================================
 * 1. JSON 解析中介層
 * ======================================================= */
app.use(express.json());

/* =========================================================
 * 2. 健康檢查端點
 * ======================================================= */
app.get("/healthz", (_, res) => {
  res.json({
    status: "ok",
    service: "websocket-hub",
    timestamp: new Date().toISOString()
  });
});

/* =========================================================
 * 3. Socket.IO：純粹的事件中繼
 * ======================================================= */
const http = require("http").createServer(app);
const io = require("socket.io")(http, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

io.on("connection", (socket) => {
  console.log(`[Socket] 客戶端已連線：${socket.id}`);

  /* 轉送所有事件（排除發送者自己） */
  socket.onAny((event, ...args) => {
    console.log(`[中繼] ${event}:`, args);
    socket.broadcast.emit(event, ...args);
  });

  socket.on("disconnect", () => {
    console.log(`[Socket] 客戶端已斷線：${socket.id}`);
  });
});

/* =========================================================
 * 4. 伺服器啟動
 * ======================================================= */
http.listen(PORT, () => {
  console.log("=".repeat(60));
  console.log(`[WebSocket Hub] 運行於 http://0.0.0.0:${PORT}`);
  console.log(`[WebSocket Hub] Socket.IO 中繼已啟用`);
  console.log("=".repeat(60));
});

/* =========================================================
 * 5. 優雅關閉處理
 * ======================================================= */
const shutdown = (signal) => {
  console.log(`\n[WebSocket Hub] 收到 ${signal}，正在關閉...`);
  http.close(() => {
    console.log("[WebSocket Hub] 伺服器已關閉");
    process.exit(0);
  });
};

process.on("SIGTERM", () => shutdown("SIGTERM"));
process.on("SIGINT", () => shutdown("SIGINT"));

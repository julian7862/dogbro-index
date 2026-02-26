# WebSocket Hub Dockerfile
FROM node:18-alpine

# 設定工作目錄
WORKDIR /app

# 複製依賴檔案
COPY package*.json ./

# 安裝依賴
RUN npm ci --only=production

# 複製伺服器程式碼
COPY server.js ./

# 暴露端口
EXPOSE 3001

# 健康檢查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001/healthz', (res) => { process.exit(res.statusCode === 200 ? 0 : 1); })"

# 啟動伺服器
CMD ["node", "server.js"]

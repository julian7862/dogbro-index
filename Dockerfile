# Python 報價服務 Dockerfile
FROM python:3.12-slim

# 設定時區（台股報價時區重要）
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 設定工作目錄
WORKDIR /app

# 複製依賴檔案
COPY requirements.txt ./

# 安裝依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY main.py ./
COPY src/ ./src/

# 設定環境變數（Socket.IO 連線到 socket-hub）
ENV GATEWAY_URL=http://socket-hub:3001

# 啟動報價服務
CMD ["python", "-u", "main.py"]

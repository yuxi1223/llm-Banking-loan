# 使用 Python 3.11.9-slim-bullseye 作為基礎鏡像
FROM python:3.11.9-slim-bullseye

# 設置工作目錄
WORKDIR /LLM-BANKING-LOAN

# 將當前目錄下的所有內容複製到工作目錄中
COPY . .

# 安裝所需的套件
RUN pip install --no-cache-dir -r requirements.txt

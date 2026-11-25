FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    SERVE_FRONTEND=1

WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

WORKDIR /app/backend
EXPOSE 5000
# 绑定到 $PORT（Render 等平台会注入），本地未设置时回退到 5000。
CMD ["sh", "-c", "python -m flask run --host 0.0.0.0 --port ${PORT:-5000}"]

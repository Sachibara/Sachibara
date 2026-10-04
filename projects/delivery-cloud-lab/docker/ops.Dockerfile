FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && useradd --uid 10001 --create-home app
COPY . .
RUN mkdir -p data && chown -R app:app /app
USER app
EXPOSE 8090
CMD ["python","-m","uvicorn","asgi:app","--host","0.0.0.0","--port","8090"]

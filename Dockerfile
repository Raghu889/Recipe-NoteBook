FROM python:3.12

WORKDIR /app

COPY requirements-docker.txt .

RUN pip install --no-cache-dir -r requirements-docker.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
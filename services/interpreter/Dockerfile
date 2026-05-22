FROM python:3.10-slim

WORKDIR /app

COPY services/interpreter/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY services/interpreter/app.py app.py

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]

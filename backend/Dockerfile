FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

ENV HF_HOME=/tmp

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860", "--workers", "1"]

FROM python:3.10-slim

WORKDIR /app

# Copy everything inside backend folder
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV HF_HOME=/tmp

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "1"]
# Start with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "2"]

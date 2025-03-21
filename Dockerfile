FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Expose the metrics port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
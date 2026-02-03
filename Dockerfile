FROM python:3.11-slim

# System dependencies (agar numpy/pandas ko chahiye ho)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pehle requirements copy karein (caching ke liye achha hai)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki saara code aur model file copy karein
COPY . .

# SageMaker default port
EXPOSE 8080

# 'CMD' ko hatakar 'ENTRYPOINT' use karein
# Yeh SageMaker ki 'serve' command ko handle kar lega
ENTRYPOINT ["python", "app.py"]
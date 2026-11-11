FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements and install using only binary wheels (--only-binary=:all:)
COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt || pip install --no-cache-dir -r requirements.txt

# Install PyTorch CPU-only explicitly from the PyTorch wheel index
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY . .

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
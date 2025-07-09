FROM python:3.10-slim

WORKDIR /app

# Install Node.js and npm
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt setup.sh ./

# Run setup script which includes pip and npm installations
RUN chmod +x setup.sh && ./setup.sh

COPY . .

CMD ["python", "example.py"]
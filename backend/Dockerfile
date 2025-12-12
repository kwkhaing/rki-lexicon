# ----------------------------------------
# 1. Base image
# ----------------------------------------
FROM python:3.11-slim AS build

# Ensure pip is up to date
RUN pip install --upgrade pip

# Set working directory
WORKDIR /app

# Install OS dependencies for production grade
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy app files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# ----------------------------------------
# 2. Final runtime image (lightweight)
# ----------------------------------------
FROM python:3.11-slim AS final

WORKDIR /app

# Copy installed libraries from build image
COPY --from=build /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=build /usr/local/bin /usr/local/bin

# Copy source code
COPY --from=build /app /app

# Expose backend port
EXPOSE 8000

# Uvicorn command for production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

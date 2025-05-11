FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git cmake g++ make libx11-dev libgl1-mesa-glx libglu1-mesa freeglut3 \
    libgl1-mesa-dev libglu1-mesa-dev libfreetype6-dev libxext-dev libxi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

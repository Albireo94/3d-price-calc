# Use the official Python image from Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies for trimesh and Flask app
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app

# Set environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the Flask app port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]

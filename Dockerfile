# Use a Python 3.10 base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pythonOCC-Core from PyPI
RUN pip install pythonOCC-Core==7.5.0

# Copy your Flask app code into the container
COPY . .

# Expose the port that Flask will run on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

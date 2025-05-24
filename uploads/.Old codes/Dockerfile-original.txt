# Use CadQuery's base image
FROM cadquery/cadquery:latest

# Set the working directory
WORKDIR /app

# Copy your app code into the container
COPY . .

# Install Flask and other dependencies
RUN pip install -r requirements.txt

# Expose port 10000 for Flask or gunicorn
EXPOSE 10000

# Run the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

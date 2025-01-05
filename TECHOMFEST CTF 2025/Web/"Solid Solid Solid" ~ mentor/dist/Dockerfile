# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install the dependencies
RUN pip install --no-cache-dir Flask==3.1.0 requests

# Copy the rest of the application code
COPY . .

RUN chmod +x run.sh

# Expose the port that the Flask app runs on
EXPOSE 5000

# Set the command to run the Flask app
CMD ["./run.sh"]

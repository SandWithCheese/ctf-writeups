FROM python:3.9

WORKDIR /app

# Copy the application files
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run the application
CMD ["python", "app.py"]


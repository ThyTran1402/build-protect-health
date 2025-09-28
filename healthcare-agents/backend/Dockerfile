# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file (if you have one)
# COPY requirements.txt .

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Install any additional dependencies your app needs
# You may need to add specific packages based on your imports
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv

# Expose the port your app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
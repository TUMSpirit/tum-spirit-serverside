# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install -r requirements.txt

# Copy the FastAPI app files to the container
COPY app.py .
COPY models /app/models

# Expose the port that Uvicorn will run on
EXPOSE 8000

# Run Uvicorn 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
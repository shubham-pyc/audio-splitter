# Use a Python base image
FROM python:3.10-slim

# Install ffmpeg and other dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script and sample audio file into the container
COPY split.py /app/split.py
COPY sample.mp3 /app/sample.mp3

# Install any Python dependencies (if needed)
# For example, if you have a requirements.txt, you would uncomment this line
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# Run the Python script when the container starts
CMD ["python", "split.py"]

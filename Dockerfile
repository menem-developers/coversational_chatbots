# Use the Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory
WORKDIR /

# Install system dependencies including libmagic
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    file \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY ./requirements.txt /requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# Copy the entire application code into the container
COPY ./ /

# Set the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

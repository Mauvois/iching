# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install gcc and other necessary build tools
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8080

# Expose the port Streamlit will run on
EXPOSE 8501

# Run both FastAPI and Streamlit
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8080 & streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0"]

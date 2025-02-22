# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that Streamlit uses
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.enableCORS", "false"]

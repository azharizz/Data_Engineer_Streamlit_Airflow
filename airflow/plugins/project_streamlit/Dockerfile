# Use the official Python base image with the desired Python version
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the current directory to the container
COPY . .

# Expose the port that Streamlit listens on (default is 8501)
EXPOSE 8501

# Run the Streamlit app when the container starts
CMD ["streamlit", "run", "--server.port", "8501", "Hello.py"]

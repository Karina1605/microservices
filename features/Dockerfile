# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /features

# Copy the current directory contents into the container at /app
COPY . /features

# Install any needed dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container (if needed)
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "features.py"]
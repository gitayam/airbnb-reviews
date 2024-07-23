# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the port available to the world outside this container
EXPOSE ${PORT_NUMBER}

# Run the Flask app when the container launches
# running the app in the app directory
CMD ["python", "app/app.py"] 
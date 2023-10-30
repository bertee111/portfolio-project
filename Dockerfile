# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /portfolioproject

# Copy the Flask application code into the container
COPY . /portfolioproject/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Define the Flask app environment variable
ENV FLASK_APP=app

# Set the Flask app to run in production mode
ENV FLASK_ENV=developement

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
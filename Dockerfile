# Use an official Python runtime as a parent image
FROM python:3.9.11

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=messeges.settings
ENV POSTGRES_HOST="localhost"
ENV DB_NAME="messeges"
ENV REDIS_HOST="127.0.0.1"
ENV REDIS_PORT=6379
ENV DJANGO_SETTINGS_MODULE="messeges.settings"
ENV NODE_MAJOR=16

# Install Node.js and npm
RUN apt-get update
RUN apt-get install -y ca-certificates curl gnupg
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list

RUN apt-get update && apt-get install nodejs -y


# Copy the frontend folder into the container
COPY frontend /frontend

# Set the working directory to the frontend folder
WORKDIR /frontend

# Install frontend dependencies
RUN npm install

# Build the frontend assets
RUN npm run build

# Create and set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that the application will run on
EXPOSE 8000

# Start the application
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]

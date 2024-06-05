FROM python:3.9

# Work directory
WORKDIR /api

# Copy the requirements file to the app
COPY requirements.txt /api/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Update and install netcat
RUN apt-get update && apt-get install -y netcat-traditional

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy files in the app
COPY . /api/

# Make the script executable
RUN chmod +x /api/wait-for-db.sh

# Expose the port       
EXPOSE 8000

# Set the enviroment var for the django settings module
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Command to wait for the db and then execute the django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

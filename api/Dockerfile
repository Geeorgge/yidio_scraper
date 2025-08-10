FROM python:3.9

# Work directory
WORKDIR /api

# Copy the requirements file
COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies
RUN pip install selenium

# Copy all project files
COPY . .

# Make wait-for-db.sh executable
RUN chmod +x /api/wait-for-db.sh

# Set environment variable
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Expose port
EXPOSE 8000

# Entry point: wait for DB before running
ENTRYPOINT ["/api/wait-for-db.sh"]

# Corrected CMD: start Django dev server
CMD ["db", "python", "manage.py", "runserver", "0.0.0.0:8000"]

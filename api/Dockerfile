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

# Copy all files (including the script)
COPY . .

# Make sure wait-for-db.sh is executable
RUN chmod +x /api/wait-for-db.sh

# Set environment variable
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Expose port
EXPOSE 8000

# Entrypoint for waiting DB
ENTRYPOINT ["/api/wait-for-db.sh"]

# Start command
CMD ["db", "python", "manage.py", "runserver", "0.0.0.0:8000"]

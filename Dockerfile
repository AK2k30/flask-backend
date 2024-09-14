# Use a more recent Python version for better performance and security
FROM python:3.9-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV INSTALL_PATH /todo-backend

# Create necessary directories
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Run gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:create_app()"]
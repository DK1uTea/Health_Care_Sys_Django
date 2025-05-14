FROM python:3.9-slim

WORKDIR /app

# Install only essential dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir \
    Django==3.2.19 \
    djangorestframework==3.14.0 \
    psycopg2-binary==2.9.6 \
    requests==2.28.2 \
    gunicorn==21.2.0 \
    python-dotenv==1.0.0 \
    django-cors-headers==4.0.0 \
    dj-database-url==1.2.0 \
    numpy==1.21.0

# Copy project
COPY . .

# Create the templates directory
RUN mkdir -p /app/ai/templates/ai

# Start the service
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8006
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run migrations and start server
EXPOSE 8002
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8002"]
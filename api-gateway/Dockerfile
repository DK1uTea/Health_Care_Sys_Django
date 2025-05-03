FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run server
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
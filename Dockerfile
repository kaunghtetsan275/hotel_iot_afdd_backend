# Base image
FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /afdd_backend

# Install system deps
RUN apk update && apk add --no-cache bash nginx supervisor gettext sqlite\
    && mkdir -p /etc/nginx/conf.d /etc/nginx/templates

# Install Python deps
COPY requirements.txt /afdd_backend/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /afdd_backend/

# Set up nginx conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template

# Set up supervisord
COPY supervisord.conf /etc/supervisord.conf

# Expose dynamic port for Render
EXPOSE 10000

# Entrypoint shell script to set up Django at runtime
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]

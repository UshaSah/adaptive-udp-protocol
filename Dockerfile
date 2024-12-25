# Base image
FROM python:3.9-slim

# Install necessary tools
RUN apt-get update && apt-get install -y \
    iproute2 iputils-ping sudo net-tools procps

# Set working directory
WORKDIR /app

# Copy all scripts into the container
COPY . /app

# Make train.sh executable
RUN chmod +x /app/train.sh

# Expose the receiver port
EXPOSE 4010

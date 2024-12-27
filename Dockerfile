# Base image
FROM ubuntu:20.04

# Set non-interactive frontend for apt to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3, pip3, and necessary tools
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    iproute2 iputils-ping sudo net-tools procps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a symbolic link for python -> python3
RUN ln -s /usr/bin/python3 /usr/bin/python

# Upgrade pip and setuptools
RUN pip3 install --no-cache-dir -U pip setuptools

# Set working directory
WORKDIR /app

# Copy all scripts into the container
COPY . /app

# Make train.sh executable
RUN chmod +x /app/train.sh

# Expose the port for the receiver
EXPOSE 4010

# Default entry point

CMD ["bash"]
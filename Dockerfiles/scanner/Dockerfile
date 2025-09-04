# Use Ubuntu base image
FROM ubuntu:latest

# Install nmap and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends nmap && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /scanner

# Keep container alive
CMD ["tail", "-f", "/dev/null"]
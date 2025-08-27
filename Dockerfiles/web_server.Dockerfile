FROM ubuntu:22.04

# Install updates and nginx
RUN apt update && apt install -y openssh-server && apt install -y iputils-ping && apt clean

# Expose HTTP port
EXPOSE 80

# Run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
FROM ubuntu:22.04

# Install updates and ssh server
RUN apt update && apt install -y openssh-server && apt install -y iputils-ping && apt clean

# Create SSH directory and set root password
RUN mkdir /var/run/sshd && echo 'root:password123' | chpasswd

# Allow root login (only for test, insecure in real life!)
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

# Run sshd in foreground
CMD ["/usr/sbin/sshd", "-D"]

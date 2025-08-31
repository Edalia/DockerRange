FROM alpine:latest

# Install tools for BYOD and server scanning
RUN apk add --no-cache \
    nmap \
    netcat-openbsd \
    curl \
    wget \
    openssl \
    tcpdump \
    net-snmp-tools \
    samba-client

# Keep container running
CMD ["tail", "-f", "/dev/null"]
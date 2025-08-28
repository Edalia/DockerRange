
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends vsftpd ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Minimal secure(ish) config: no anonymous, log, sandbox on
COPY vsftpd.conf /etc/vsftpd.conf

# Create a simple read-only directory to serve
RUN useradd -m ftpuser && \
    mkdir -p /srv/ftp && \
    chown -R ftpuser:ftpuser /srv/ftp

EXPOSE 21
CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]

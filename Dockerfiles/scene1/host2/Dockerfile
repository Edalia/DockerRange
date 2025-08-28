# Older base; leave packages behind on purpose
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends vsftpd && \
    rm -rf /var/lib/apt/lists/*

# Insecure config: anonymous enabled, sandbox off
COPY vsftpd.conf /etc/vsftpd.conf

EXPOSE 21
CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]

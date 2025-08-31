FROM ubuntu:14.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends vsftpd bash && rm -rf /var/lib/apt/lists/* 

COPY vsftpd.conf /etc/vsftpd.conf 

EXPOSE 21

RUN apt-get update && apt-get install -y iputils-ping bash

# Keep container running by default
CMD ["tail", "-f", "/dev/null"]
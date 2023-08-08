FROM debian:bookworm

LABEL maintainer="Bohdan Bobyr" \
      email="bodicheg@gmail.com"

RUN apt update && \
    apt install -y \
    traceroute \
    whois \
    host \
    htop \
    dnsutils \
    telnet \
    zsh \
    curl \
    iputils-ping \
    git-core \
    git \
    tree \
    openvpn \
    python3 \
    python3-pip \
    libcurl4-openssl-dev \
    libssl-dev \
    nmap \
    masscan \ 
    ssh \ 
    smbclient

# Install python dependencies
COPY packages.list /tmp
RUN \
    pip install -r /tmp/packages.list --break-system-packages

# Run jupiter
EXPOSE 8888
CMD ["jupyter", "server", "--ip='0.0.0.0'", "--port=8888", "--allow-root", "--notebook-dir=/root"]

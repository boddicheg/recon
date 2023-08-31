FROM ubuntu
ARG DEBIAN_FRONTEND=noninteractive

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
    python3-venv \
    libcurl4-openssl-dev \
    libssl-dev \
    nmap \
    masscan \ 
    ssh \ 
    smbclient \
    iproute2 \ 
    nodejs \
    npm

# Install python dependencies
COPY packages.list /tmp
RUN \
    python3 -m venv /root/.local/venv
RUN \
    /root/.local/venv/bin/pip install -r /tmp/packages.list

# Run jupiter
EXPOSE 8888
EXPOSE 80

# Custom cache invalidation
ARG CACHEBUST=1

CMD ["/root/.local/venv/bin/jupyter-server", "--ip='0.0.0.0'", "--port=8888", "--allow-root", "--notebook-dir=/root"]
# CMD [ "ls", "-la", "/root/.local/venv/bin" ]


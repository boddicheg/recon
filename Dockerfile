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
    ssh

# OS TOOLS
# Install oh-my-zsh
RUN \
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended && \
    sed -i '1i export LC_CTYPE="C.UTF-8"' /root/.zshrc && \
    sed -i '2i export LC_ALL="C.UTF-8"' /root/.zshrc && \
    sed -i '3i export LANG="C.UTF-8"' /root/.zshrc && \
    sed -i '3i export LANGUAGE="C.UTF-8"' /root/.zshrc && \
    git clone --depth 1 https://github.com/zsh-users/zsh-autosuggestions /root/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
    git clone --depth 1 https://github.com/zsh-users/zsh-syntax-highlighting.git /root/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting && \
    git clone --depth 1 https://github.com/zsh-users/zsh-history-substring-search /root/.oh-my-zsh/custom/plugins/zsh-history-substring-search && \
    sed -i 's/plugins=(git)/plugins=(git aws golang nmap node pip pipenv python ubuntu zsh-autosuggestions zsh-syntax-highlighting zsh-history-substring-search)/g' /root/.zshrc && \
    sed -i '78i autoload -U compinit && compinit' /root/.zshrc

# Install python dependencies
COPY packages.list /tmp
RUN \
    pip install -r /tmp/packages.list --break-system-packages

# Run jupiter
EXPOSE 8888
CMD ["jupyter", "notebook", "--ip='0.0.0.0'", "--port=8888", "--allow-root"]

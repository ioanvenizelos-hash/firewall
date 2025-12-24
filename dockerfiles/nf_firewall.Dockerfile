FROM python:3.11.2

WORKDIR /firewall

RUN apt-get update && \
    apt-get install -y \
    isc-dhcp-server \
    iptables \
    iproute2 \
    net-tools \
    nmap \
    iputils-ping \
    tcpdump \
    iputils-ping \
    python3 \
    python3-pip \
    python3-venv \
    ulogd2 \
    vim \
    logrotate \
    procps \
    nftables \
    vlan \
    ifupdown \
    kmod \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY generated_from_j2 ./generated_from_j2
COPY templates ./templates
COPY main.py .
COPY firewall_api.py .
COPY interfaces_api.py .
COPY entrypoint.sh /firewall/entrypoint.sh
RUN chmod +x /firewall/entrypoint.sh


CMD ["/firewall/entrypoint.sh"]


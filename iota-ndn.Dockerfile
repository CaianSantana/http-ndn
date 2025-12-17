############################
# Stage 1 — IOTA builder
############################
FROM alpine:3.22 AS iota-builder

WORKDIR /iota

RUN apk update && \
    apk add wget tar curl unzip libpq-dev libudev-zero

ENV IOTA_VERSION="v1.7.0"

RUN wget -O iota-binaries.tgz \
      https://github.com/iotaledger/iota/releases/download/${IOTA_VERSION}/iota-${IOTA_VERSION}-linux-x86_64.tgz && \
    tar -xzvf iota-binaries.tgz && \
    rm iota-binaries.tgz


############################
# Stage 2 — Final image
############################
FROM ubuntu:22.04

WORKDIR /app
COPY . .

# ===== System deps =====
RUN apt-get update && \
    apt-get install -y software-properties-common python3 python3-pip \
                       libcap2-bin sqlite3 curl libpq-dev && \
    add-apt-repository -y ppa:named-data/ppa && \
    apt-get update && \
    apt-get install -y nfd ndn-tools && \
    rm -rf /var/lib/apt/lists/*

# ===== IOTA binary =====
COPY --from=iota-builder /iota /usr/local/bin

# ===== NDN user & socket =====
RUN usermod -d /var/lib/ndn ndn && \
    mkdir -p /var/lib/ndn/.ndn /run/nfd && \
    chown -R ndn:ndn /var/lib/ndn /run/nfd && \
    ln -s /run/nfd/nfd.sock /var/run/nfd.sock && \
    setcap cap_net_raw+eip /usr/bin/nfd

EXPOSE 6363/udp 8080 9000 9123

# ===== NFD config =====
COPY nfd.conf /etc/ndn/nfd.conf

# ===== App perms =====
RUN chown -R ndn:ndn /app

# ===== Entrypoint =====
COPY entrypoint-iota-ndn.sh /entrypoint-iota-ndn.sh
RUN chmod +x /entrypoint-iota-ndn.sh

# ===== NDN keys =====
USER ndn
RUN ndnsec key-gen -t r /app && \
    ndnsec cert-dump -i /app > app-trust-anchor.cert && \
    ndnsec key-gen -t r /app && \
    ndnsec sign-req /app | ndnsec cert-gen -s /app -i app | ndnsec cert-install -

# ===== Python deps =====
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/entrypoint-iota-ndn.sh"]

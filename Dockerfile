FROM ubuntu:22.04

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:named-data/ppa && \
    apt-get update && \
    apt-get install -y nfd ndn-tools libcap2-bin python3-pip sqlite3 && \
    rm -rf /var/lib/apt/lists/*

RUN usermod -d /var/lib/ndn ndn
RUN mkdir -p /var/lib/ndn/.ndn && \
    chown -R ndn:ndn /var/lib/ndn

RUN chown ndn:ndn /usr/bin/nfd
RUN mkdir -p /run/nfd && chown ndn:ndn /run/nfd
RUN ln -s /run/nfd/nfd.sock /var/run/nfd.sock
EXPOSE 6363/udp
RUN setcap cap_net_raw+eip /usr/bin/nfd

RUN chown -R ndn:ndn /app

RUN echo 'log\n\
{\n\
  default_level INFO\n\
}\n\
tables\n\
{\n\
  cs_max_packets 65536\n\
}\n\
face_system\n\
{\n\
  unix\n\
  {\n\
    path /run/nfd/nfd.sock\n\
  }\n\
  udp\n\
  {\n\
    port 6363\n\
  }\n\
  ether\n\
  {\n\
    mcast yes\n\
  }\n\
}\n\
authorizations\n\
{\n\
  authorize\n\
  {\n\
    certfile any\n\
    privileges\n\
    {\n\
      faces\n\
      fib\n\
      cs\n\
      strategy-choice\n\
    }\n\
  }\n\
}\n\
rib\n\
{\n\
  localhost_security\n\
  {\n\
    rule\n\
    {\n\
      id "any-interaction"\n\
      for interest\n\
      filter\n\
      {\n\
        type name\n\
        regex ^<>*$\n\
      }\n\
      checker\n\
      {\n\
        type customized\n\
        sig-type rsa-sha256\n\
        key-locator\n\
        {\n\
          type name\n\
          regex ^<>*$\n\
        }\n\
      }\n\
    }\n\
    trust-anchor\n\
    {\n\
      type any\n\
    }\n\
  }\n\
}' > /etc/ndn/nfd.conf

USER ndn

RUN ndnsec key-gen -t r /app
RUN ndnsec cert-dump -i /app > app-trust-anchor.cert
RUN ndnsec key-gen -t r /app
RUN ndnsec sign-req /app | ndnsec cert-gen -s /app -i app | ndnsec cert-install -

RUN pip install -r requirements.txt

CMD ["nfd"]
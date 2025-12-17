#!/bin/bash
set -e

echo "[1] NFD..."
nfd &

echo "[2] Aguardando NFD..."
until [ -S /run/nfd/nfd.sock ]; do
  sleep 0.2
done

echo "[3] Quart adapter..."
python3 -m quart --app app.py run --host 0.0.0.0 --port 8080 &

echo "[4] IOTA node..."
exec /usr/local/bin/iota start --force-regenesis --with-faucet

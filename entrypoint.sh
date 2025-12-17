#!/bin/bash
set -e

echo "Iniciando NFD..."
nfd &

echo "Aguardando NFD..."
for i in {1..30}; do
    if [ -S /run/nfd/nfd.sock ]; then
        echo "NFD pronto!"
        break
    fi
    sleep 0.2
done

echo "Iniciando Gateway HTTP-NDN (Quart)..."
exec python3 -m quart --app app.py run --host 0.0.0.0 --port 8080
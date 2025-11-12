Criar e usar ambiente virtual

    python3 -m venv .venv
    . .venv/bin/activate

Instalar bibliotecas

    pip install -r requirements.txt

Iniciar servidor na porta 8080    

    flask run --port 8080 --host=0.0.0.0

Fazer requisição

    curl --location --request POST 'http://127.0.0.1:8080/node/1' \
    --header 'Content-Type: application/json' \
    --data-raw '{"jsonrpc": "2.0","id": 1,"method": "iota_getTotalTransactionBlocks","params": []}'
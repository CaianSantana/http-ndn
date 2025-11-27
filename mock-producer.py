import logging
import asyncio
import os
from ndn.app import NDNApp
from ndn.encoding import Name, Component
from ndn.security import KeychainDigest

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

os.environ['NDN_CLIENT_TRANSPORT'] = 'unix:///run/nfd/nfd.sock'

app = NDNApp(keychain=KeychainDigest())

@app.route('/br/ba/ssa/iota/first')
def on_interest(name, interest_param, application_param):
    print(f"Recebi interesse para: {Name.to_str(name)}")
    
    if application_param:
        print(f"Payload recebido: {bytes(application_param).decode('utf-8')}")

    content = "Resposta do Blockchain: Bloco #12345 (Via NDN)"
    app.put_data(name, content=content.encode('utf-8'), freshness_period=10000)
    print("Dados enviados!")

if __name__ == '__main__':
    print("Iniciando Produtor Mock...")
    app.run_forever()
import asyncio
import os
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam
from ndn.security import KeychainDigest
import requester


def connect_nfd():
    os.environ['NDN_CLIENT_TRANSPORT'] = 'unix:///run/nfd/nfd.sock'
    
    return NDNApp(keychain=KeychainDigest())

async def consume(app, interest_name, must_be_fresh=True, can_be_prefix=False, lifetime=6000, ApplicationParameters=None):
    try:
        int_param = InterestParam(must_be_fresh=must_be_fresh, lifetime=lifetime)

        app_param_bytes = None
        if ApplicationParameters:
            if isinstance(ApplicationParameters, bytes):
                app_param_bytes = ApplicationParameters
            elif isinstance(ApplicationParameters, str):
                app_param_bytes = ApplicationParameters.encode('utf-8')
            elif isinstance(ApplicationParameters, dict):
                import json
                app_param_bytes = json.dumps(ApplicationParameters).encode('utf-8')

        print(f"Expressando interesse: {Name.to_str(interest_name)}")

        data_name, meta_info, content = await app.express_interest(
            interest_name,
            interest_param=int_param,   
            app_param=app_param_bytes,  
            validator=None
        )

        if content:
            return bytes(content).decode('utf-8')
        return {"status": "sem conteudo"}

    except Exception as e:
        print(f"Erro no consume: {e}")
        return {"error": str(e), "type": str(type(e))}
    
def make_handler(ndn_app):
    def on_interest(name, interest_param, application_param):
        asyncio.create_task(
            handle_interest_async(ndn_app, name, application_param)
        )
    return on_interest

async def handle_interest_async(ndn_app, name, application_param):
    print(f"Recebi interesse para: {Name.to_str(name)}")

    content = "payload vazio"

    if application_param:
        payload = bytes(application_param)
        print(f"Payload recebido: {payload.decode('utf-8')}")
        content = await requester.post(payload)

    ndn_app.put_data(
        name,
        content=content.encode('utf-8'),
        freshness_period=10000
    )

    print("Dados enviados!")

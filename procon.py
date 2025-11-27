import asyncio
import os
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam
from ndn.security import KeychainDigest

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
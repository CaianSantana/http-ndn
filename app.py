from quart import Quart, request, jsonify
from selector import select_name
from procon import connect_nfd, consume, make_handler
import asyncio
import os

app = Quart(__name__)
ndn_app = None
NODE_ID = None


@app.before_serving
async def startup():
    global ndn_app, NODE_ID

    NODE_ID = os.getenv("NODE_ID")
    if NODE_ID is None:
        raise RuntimeError("NODE_ID não definido (ex: NODE_ID=1)")

    NODE_ID = int(NODE_ID)

    print(f"Iniciando Gateway HTTP-NDN para node {NODE_ID}...")

    ndn_app = connect_nfd()

    loop = asyncio.get_event_loop()
    loop.create_task(ndn_app.main_loop())

    prefix = select_name(NODE_ID)
    ndn_app.route(prefix)(make_handler(ndn_app))

    print(f"Prefixo registrado: {prefix}")

    print("Aguardando conexão com o NFD...")
    for _ in range(20):
        if ndn_app.face.running:
            print("Conectado ao NFD via Socket com sucesso!")
            break
        await asyncio.sleep(0.1)
    else:
        print("ALERTA: conexão com NFD não confirmada")


@app.post("/node/<int:node_id>")
async def node_post(node_id):
    global ndn_app

    if ndn_app is None or not ndn_app.face.running:
        return jsonify({"error": "Gateway NDN desconectado"}), 503

    name = select_name(node_id)

    raw_data = await request.get_data()

    print(f"[HTTP -> NDN] Enviando {len(raw_data)} bytes para: {name}")

    response = await consume(ndn_app, name, ApplicationParameters=raw_data)

    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")

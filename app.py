from flask import Flask, json, request
from markupsafe import escape
from selector import select_name
from procon import connect_nfd, start_loop, consumer, producer
import ast
import asyncio

app = Flask(__name__)

async def start_ndn_stack():
  ndn_app = connect_nfd()
  start_loop(ndn_app)


@app.post("/node/<int:node_id>")
async def node_post(node_id):
  name = select_name(node_id)
  if len(request.get_data()) == 0:
      request_body = ""
  else:
      request_body = ast.literal_eval(request.get_data().decode("UTF-8"))
  print(repr(request_body))
  return json.jsonify(consumer(name, request_body))


start_ndn_stack()

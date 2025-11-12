from flask import Flask, json, request
from markupsafe import escape
from selector import select_name
from ndn import consumer
import ast


app = Flask(__name__)

@app.post("/node/<int:node_id>")
def node_post(node_id):
    name=select_name(node_id)
    if len(request.get_data()) == 0:
        request_body = ""
    else:
        request_body=ast.literal_eval(request.get_data().decode("UTF-8"))
    print(repr(request_body))
    return json.jsonify(consumer(name, request_body))


'''
curl --location --request POST 'http://127.0.0.1:9000' \
--header 'Content-Type: application/json' \
--data-raw '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "iota_getTotalTransactionBlocks",
  "params": []
}'
'''
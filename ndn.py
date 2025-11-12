
'''
{
  "jsonrpc": "2.0",
  "id": 0,
  "result": {
    "openrpc": "1.2.6",
    "info": {
      "title": "Mock",
      "version": "1.0.0"
    },
    "methods": [
      {
        "name": "info",
        "summary": "Retorna info do nó"
      }
    ]
  }
}
'''

def consumer(name, request_body):
    if len(request_body) == 0:
        return "request vazia..."
    app_param=convert_to_json(request_body)

    return send_interest(name, app_param)

def convert_to_json(dictionary):
    return dictionary

def send_interest(name, app_param):
    response = {"jsonrpc": "2.0","id": 0,"result": {"openrpc": "1.2.6","info": {"title": "Mock","version": "1.0.0"},"methods": [{"name": "info","summary": "Retorna info do nó"}]}}
    return response

'''
{
  "jsonrpc": "2.0",
  "result": 168,
  "id": 1
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
    response = {"jsonrpc": "2.0", "result": 168, "id": 1}
    return response
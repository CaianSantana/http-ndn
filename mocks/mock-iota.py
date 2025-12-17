from quart import Quart
import ast
import asyncio

app = Quart(__name__)
ndn_app = None


@app.post("/")
async def post():
    print("http://localhost:9000 post recebido!")
    return "OK!"

if __name__ == "__main__":
    app.run(port=9000, host="0.0.0.0")
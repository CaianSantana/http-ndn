from ndn.app import NDNApp
app = NDNApp()

@app.route('br/ba/ssa/iota/first')
def on_interest(name, interest_param, application_param):
    app.put_data(name, content=b'content', freshness_period=10000)

app.run_forever()

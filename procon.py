from ndn.app import NDNApp
from ndn.encoding import Name

def connect_nfd():
  return NDNApp()

async def start_loop(app):
  app.run_forever()

async def consume(app, interest_name, must_be_fresh=True, can_be_prefix=False, lifetime=6000, ApplicationParameters=None):
    try:
        data_name, meta_info, content = await app.express_interest(
            # Interest Name
            interest_name,
            must_be_fresh,
            can_be_prefix,
            # Interest lifetime in ms
            lifetime,
            ApplicationParameters)
        # Print out Data Name, MetaInfo and its conetnt.
        print(f'Received Data Name: {Name.to_str(data_name)}')
        print(meta_info)
        print(bytes(content) if content else None)
    except InterestNack as e:
        # A NACK is received
        print(f'Nacked with reason={e.reason}')
    except InterestTimeout:
        # Interest times out
        print(f'Timeout')
    except InterestCanceled:
        # Connection to NFD is broken
        print(f'Canceled')
    except ValidationFailure:
        # Validation failure
        print(f'Data failed to validate')
    finally:
        app.shutdown()

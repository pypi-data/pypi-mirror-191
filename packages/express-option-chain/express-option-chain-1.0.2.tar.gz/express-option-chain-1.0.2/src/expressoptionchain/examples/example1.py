from expressoptionchain.option_stream import OptionStream
from expressoptionchain.helper import get_secrets

# the option stream start should be in main module
if __name__ == '__main__':
    secrets = {
        'api_key': get_secrets()['api_key'],
        'access_token': get_secrets()['access_token']
    }
    # there is no limit on the number of symbols to subscribe to
    symbols = ['NFO:HDFCBANK', 'NFO:INFY', 'NFO:RELIANCE', 'NFO:DRREDDY', 'NFO:EICHERMOT']
    # symbols = ['CDS:EURINR', 'CDS:GBPINR', 'CDS:JPYINR', 'CDS:USDINR', 'BCD:EURINR']
    # symbols = ['MCX:GOLD', 'MCX:GOLDM', 'MCX:NATURALGAS', 'MCX:NICKEL', 'MCX:SILVER', 'MCX:SILVERM']

    stream = OptionStream(symbols, secrets, expiry='23-02-2023')
    stream.start()

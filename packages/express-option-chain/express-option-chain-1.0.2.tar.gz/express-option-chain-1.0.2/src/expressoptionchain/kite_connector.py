from expressoptionchain.helper import get_secrets
from kiteconnect import KiteConnect
import logging

log = logging.getLogger(__name__)

class KiteConnectionManager:
    __kite_client = None

    def __init__(self, api_key, access_token):
        log.info('Creating kite client')
        secrets = get_secrets()
        kite_client = KiteConnect(api_key=secrets['api_key'])
        kite_client.set_access_token(secrets['access_token'])
        KiteConnectionManager.__kite_client = kite_client

    @staticmethod
    def get_kite_client(api_key, access_token):
        if not KiteConnectionManager.__kite_client:
            KiteConnectionManager(api_key, access_token)
        return KiteConnectionManager.__kite_client


class KiteConnector:
    def __init__(self, api_key: str, access_token: str) -> None:
        self.kite_client = KiteConnectionManager.get_kite_client(api_key, access_token)

    def get_ltp(self, trading_symbols: list[str]) -> dict[str, dict[str, float]]:
        '''
        :param trading_symbols: list of trading symbols of format exchange:trading_symbol e.g. NSE:ACC
        :return: map of trading symbol to the ltp quote e.g. {'NSE:ACC': {'instrument_token': 5633, 'last_price': 1880.4}}
        '''
        return self.kite_client.ltp(trading_symbols)

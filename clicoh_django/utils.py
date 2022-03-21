from datetime import datetime, timedelta
from decimal import Decimal
import requests

HOURS_TO_UPDATE = 2

class UsdFetcher():
    """
    The purpose of this class is to fetch the current value of the US dollar
    and store it in a internal variable 'self._dolar_blue'.
    
    This prevents to the app to make too many requests to the dolarsi website
    and makes the responses faster.
    
    Usage: just call settings.USD_FETCHER.get_dolar_blue() -> Decimal
    
    The app will update the value of the 'Dolar blue' every 2 hours (if demanded)
    
    The value of 2 Hours is hardcodded in the 'HOURS_TO_UPDATE' constant
    """
    
    def __init__(self) -> None:
        self._dolar_blue = {
            'value': Decimal('0.0'),
            'expiration': datetime.now()
        }
        pass
    
    
    def get_dolar_blue(self) -> Decimal:
        """
        Returns the Decimal value of 'Dolar Blue'.
        If the value is expired, it will be updated before returning.
        """
        if self._dolar_blue['expiration'] < datetime.now():
            self._dolar_blue = {
                'value': self.get_usd_dolarsi(),
                'expiration': datetime.now()+timedelta(hours=HOURS_TO_UPDATE)
            }
        return self._dolar_blue['value']

    
    def get_usd_dolarsi(self) -> Decimal:
        """
        Fetch the DolarSi API and retunrs the Decimal value of 'Dolar Blue'.
        """
        url = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
        
        response = requests.get(url)
        response.raise_for_status() # check status code of response
        response = response.json() # convert to json
        value = 0.
        for item in response:
            if item["casa"]["nombre"] == 'Dolar Blue':
                value = item["casa"]["compra"]
        value = value.replace(',', '.')
        value = Decimal(value)
        return value
    
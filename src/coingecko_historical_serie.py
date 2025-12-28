"""
This module provides financial time series by requesting data from CoinGecko
and returning it as a pandas DataFrame.

This module does not use third-party modules as it makes requests via
GET only.
"""

import requests
import pandas as pd


def historical_time_series(
        symbol: str,
        vs_currency: str = 'usd',
        days: str = '365',
        interval: str = 'daily'
)-> pd.DataFrame:
    """
    Retrieves the historical time series for an asset.

    Parameters
    ----------
    symbol : str
        String containing the ID of the cryptocoin.
    vs_currency : str
        The quote currency used. Default is 'usd'.
    days : str
        Number of days to retrieve. Default is '365'.
    interval: str
        The interval of each data. Default value is 'daily'.

    Returns
    -------
    pandas.DataFrame
       DataFrame containing the historical time series with 'price' as column
       and datetime index.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    parameters = {'vs_currency': vs_currency, 'days': days, 'interval': interval}
    
    response = requests.get(url, params=parameters)
    response.raise_for_status()

    data = response.json()

    # Extract prices from the json. Prices is a list with columns ['timestamp', 'price']
    prices = data.get('prices',[])

    # Create a pd.DataFrame from the extracted price.
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('datetime', inplace=True)
    df.sort_index(inplace=True)
    df.drop('timestamp', axis=1, inplace=True)

    return df
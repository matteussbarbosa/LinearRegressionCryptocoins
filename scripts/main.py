"""
Run the main analysis workflow for linear regression on cryptocurrencies.
"""

import os
import sys
import numpy as np

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from src.coingecko_historical_serie import historical_time_series


blockchain_name_list = ['bitcoin', 'ethereum']

for asset in blockchain_name_list:
    if asset == blockchain_name_list[0]:
        bitcoin_df = historical_time_series(asset, 'usd', '365', 'daily')
    elif asset == blockchain_name_list[1]:
        ethereum_df = historical_time_series(asset, 'usd', '365', 'daily')

# Retrieves logarithmic values for each asset.
bitcoin_returns = np.log(bitcoin_df['price']).diff().dropna()
ethereum_returns = np.log(ethereum_df['price']).diff().dropna()

# Retrieves values from the DataFrames.
returns_aligned_df = (
    bitcoin_returns
    .to_frame(name='btc')
    .join(ethereum_returns.to_frame(name='eth'), how='inner')
)

X = returns_aligned_df['btc'].values
Y = returns_aligned_df['eth'].values

# Retrieves the values for the regression equation.

beta_1, beta_0 = np.polyfit(X, Y, 1)

print(f'The equation is y = {beta_0} + {beta_1} * x')
print('If the value of beta_1 (slope) is greater than zero,' \
'they have positive linear relationship.')
print('If beta_1 (slope) signal is positive,' \
'both cryptocurrencies augmentates in the same direction.')
print(f'Magnitude: {abs(beta_1)}')
print('Model limitations: errors do not fit the criteria.' \
'Data is current spot price. Absence of inference')
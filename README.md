# pythonmatrix

Script example that interacts with different APIs and displays the information on the AWTRIX matrix led.
It also follows the Bitcoin 24h/change price and modifies the Awtrix clock color to red if Bitcoin is down and to green if up.

APIs:
Prices that are displayed: Bitcoin, Ethereum, Sonos stock, Gold (XAU).

- API for crypto: Cryptocompare https://min-api.cryptocompare.com/documentation
Free, it does not require an API key for the info that I need.

- API for stock and gold price: Alphavantage https://www.alphavantage.co/documentation/
Free but requires an API key for the needed information.

Every 5 minutes, prices are checked, Clock color is modified (if needed) and prices info are pushed on the matrix with their respective colors.

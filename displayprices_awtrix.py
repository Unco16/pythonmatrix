import requests
import apscheduler
import time

from apscheduler.schedulers.blocking import BlockingScheduler

# Alpha vantage API details
alphakey = 'GN73Y41O0RZRAR73'
sono_url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=SONO&apikey=GN73Y41O0RZRAR73'
gold_url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=XAU&to_currency=USD&apikey=GN73Y41O0RZRAR73'

# Awtrix API URL settings
awtrix_api_url = 'http://192.168.0.112:7000/api/v3/settings'
# Awtrix API URL notify
awtrix_api_url_notify = 'http://192.168.0.112:7000/api/v3/notify'

# Cryptocompare API URLS
btc_url = 'https://min-api.cryptocompare.com/data/generateAvg?fsym=BTC&tsym=USD&e=Kraken'
eth_url = 'https://min-api.cryptocompare.com/data/generateAvg?fsym=ETH&tsym=USD&e=Kraken'

# Define Awtrix textcolor
red = {"TextColor":"255,0,0"}
green = {"TextColor":"0,255,0"}


#Check the bitcoin price and adjust Awtrix text color in red or green depends if BTC is up or down the last 24h
def checkprice_updatecolor():
    # Check BTC 24h Price change 
    r = requests.get(btc_url)
    data_btc = r.json()
    btc_change = data_btc['RAW']['CHANGE24HOUR']

    # Adjust Awtrix text color in red or green depends if BTC is up or down the last 24h
    if (btc_change > 0):
        requests.post(awtrix_api_url, json = green)
    elif (btc_change < 0):
        requests.post(awtrix_api_url, json = red)

        
#Check different prices (btc,eth,sonos stock,gold) through different APIs and displays them on Awtrix      
def prices_display():
    rbtc = requests.get(btc_url)
    btc_price = str(rbtc.json()['RAW']['PRICE'])
    
    reth = requests.get(eth_url)
    eth_price = str(reth.json()['RAW']['PRICE'])

    rsonos = requests.get(sono_url)
    sonos_price = rsonos.json()['Global Quote']['05. price']
    sonos_price = sonos_price[:5]

    rgold = requests.get(gold_url)
    gold_price = rgold.json()["Realtime Currency Exchange Rate"]['5. Exchange Rate']
    gold_price = str(int(float(gold_price)))

    tosend = {"force":True, "multiColorText":[{"text":"BTC: " + btc_price +"  -","color":[255,165,0]},{"text":"  ETH: " + eth_price +"  -","color":[128,128,128]},{"text":"  SONOS: " + sonos_price +"  -","color":[255,255,255]},{"text":"  GOLD: " + gold_price +" ","color":[255,255,0]}]}
    requests.post(url = awtrix_api_url_notify, json = tosend)        

    
scheduler = BlockingScheduler()

# Run btc checkprice_updatecolor and prices_display every 5 minutes
scheduler.add_job(checkprice_updatecolor, 'interval', minutes=5, args=None)
scheduler.add_job(prices_display, 'interval', minutes=5, args=None)
scheduler.start()

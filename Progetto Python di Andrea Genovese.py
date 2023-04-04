import requests
from pprint import pprint
import time
from datetime import datetime
import json

class Bot:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': 1,
            'limit': None,
            'convert': 'USD',
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'Past your CoinMarketCap key'
        }
        
    def fetchCurrenciesData(self): #richiesta alle API di coinmarketcap
        r = requests.get(url=self.url, params= self.params, headers=self.headers).json()
        return r['data']

my_bot = Bot()

while(1):
    now = datetime.now()
    my_bot.params = {
            'start': 1,
            'limit': None,
            'convert': 'USD',
    }
    currencies = my_bot.fetchCurrenciesData()
    Bestcurrency = None
    
    for currency in currencies: #Cerco la criptovaluta con il volume maggiore delle ultime 24h
        if not Bestcurrency or currency['quote'] ['USD'] ['volume_24h'] > Bestcurrency['quote'] ['USD'] ['volume_24h']:
            Bestcurrency = currency
    result1 = f"La Criptovaluta con il volume maggiore e\': {Bestcurrency['name']}.\
Il valore e\' di {Bestcurrency['quote'] ['USD'] ['volume_24h']} $"
    print(result1)

    #imposto nuovamente i parametri per ordinare i risultati nel modo in cui mi serve
    my_bot.params = {'start': 1,
            'limit': 10,
            'convert': 'USD',
            'sort': 'percent_change_24h',
            'sort_dir': 'desc'
    }
    currencies = my_bot.fetchCurrenciesData()
    best = []
      
    for currency in currencies: 
        best.append(currency['name'])
    result2 = f'Le migliori 10 criptovalute per incremento in percentuale delle ultime 24 ore sono: {best}'   
    print(result2) #le migliori 10 criptovalute
        
    my_bot.params = {'start': 1,
            'limit': 10,
            'convert': 'USD',
            'sort': 'percent_change_24h',
            'sort_dir': 'asc'
    }
    currencies = my_bot.fetchCurrenciesData()
    worst = []

    for currency in currencies: 
        worst.append(currency['name'])
    result2bis = f'Le peggiori 10 criptovalute per incremento in percentuale delle ultime 24 ore sono: {worst}'
    print(result2bis) #le peggiori 10 cryptovalute
    
    my_bot.params = {'start': 1,
            'limit': 20,
            'convert': 'USD'
    }
    currencies = my_bot.fetchCurrenciesData()
    currencies_price = []
    
    for currency in currencies: #cerco la quantità necessaria per acquistare un'unità delle prime 20 criptovalute
        currencies_price.append(currency['quote']['USD']['price'])
        sum_tot_price = sum(currencies_price)
        round_up_result = round(sum_tot_price, 2)
    result3 = f'Per acquistare una unita\' di ciascuna delle prime 20 criptovalute ho bisogno di: $ {round_up_result}'
    print(result3)
        
    my_bot.params = {'start': 1,
            'limit': None,
            'convert': 'USD',
            'volume_24h_min': 76_000_000
    }
    currencies = my_bot.fetchCurrenciesData()
    currencies_price= []
    
    for currency in currencies: #cerco la quantità necessaria per acquistare un'unità di tutte le criptovalute con un volume superiore a 76.000.000
        currencies_price.append(currency['quote']['USD']['price'])
        sum_tot_price = sum(currencies_price)
        round_up_result = round(sum_tot_price, 2)
    result4 = f'Per acquistare una unita\' di tutte le criptovalute \
il cui volume delle ultime 24h sia superiore a 76.000.000, \
ho bisogno di: $ {round_up_result}'
    print(result4)

    my_bot.params = {
            'start': 1,
            'limit': 20,
            'convert': 'USD',
            'sort': 'market_cap'
    }
    currencies = my_bot.fetchCurrenciesData()
    price_24h_ago = []
    current_price = []

    for currency in currencies:  
        round_current_price = ((round((currency['quote']['USD']['price']), 2)))
        current_price.append(round_current_price)
        round_percent_change24h = ((round((currency['quote']['USD']['percent_change_24h']), 2)))     
        #calcolo il valore di ieri prima dell'incremento % con la proporzione (Xf - Xi): Xi = % : 100 
        #con la proprietà del comporre diventa Xf : Xi = (% + 100) : 100
        x = ((round_current_price * 100)/(100 + round_percent_change24h))
        round_x = round(x, 2)          
        price_24h_ago.append(round_x) #popolo la lista con i prezzi delle crypto relativi a 24h fa
        purchase_now = round(sum(current_price), 2) #importo da pagare per acquistare ora
        purchase_24h_ago = round(sum(price_24h_ago), 2) #importo che avrei pagato 24h fa
    
        #variazione percentuale tra un eventuale acquisto effettuato 24h fa ed uno adesso
        delta = round(((purchase_now - purchase_24h_ago)/purchase_24h_ago) * 100, 2) 
    result5 = f'Se avessi comprato una unita\' per ciascuna delle prime 20 criptovalute 24h fa avrei ottenuto \
la seguente percentuale di rendimento: {delta} %'
    print(result5)

    #Salvo i risultati in un file json
    report = {
        '1': result1,
        '2': result2, 
        '2bis': result2bis,
        '3': result3,
        '4': result4,
        '5': result5
    }
    with open("project.json", "w") as outfile:
        json.dump(report, outfile, indent=6)
    
    # routine
    minutes = 1440
    seconds = minutes * 60
    time.sleep(seconds)
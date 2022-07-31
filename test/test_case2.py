import requests

url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'



def test_cas():
    price =((requests.get(url)).json())['data']['amount'] 
    currency = ((requests.get(url)).json())['data']['currency']
    base  = ((requests.get(url)).json())['data']['base']
    assert price
    assert currency
    assert base

print(  ((requests.get(url)).json())['data']['amount'],
        ((requests.get(url)).json())['data']['currency'],
        ((requests.get(url)).json())['data']['base'])
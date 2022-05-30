from time import sleep
import requests
import pandas as pd
from dictionary import conv
import concurrent.futures

header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
'referer':f'https://shopee.tw/%E5%A8%9B%E6%A8%82%E3%80%81%E6%94%B6%E8%97%8F-cat.11041645?page=0','x-api-source': 'pc'}

def Confirm ():

    base_url = "https://shopee.tw/api/v4/search/search_items?by=relevancy&fe_categoryids=11041645&limit=60&newest="

    urls = [f"{base_url}{page*60}{'&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2'}" for page in range(0, 100)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(scrape,urls)
    return results

def scrape(url):
    
    req = requests.get(url, headers = header)

    names = [req_json['item_basic']['name'] for req_json in req.json()['items']]
    prices_min = [int(req_json['item_basic']['price_min'])/10e4 for req_json in req.json()['items']]
    prices_max = [int(req_json['item_basic']['price_max'])/10e4 for req_json in req.json()['items']]

    df = pd.DataFrame({
        'name':names,'Price_min':prices_min,'Price_max':prices_max}
    )

    sleep(1)
    return df


if __name__ == '__main__':
    df_shopee = pd.DataFrame()
    results = Confirm()

    for result in results:
        df_shopee = pd.concat([df_shopee, result])

    df_shopee.to_csv('shopee_data.csv',encoding='utf-8-sig', index =False)

    conv() 


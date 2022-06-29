
import os
import requests
import pandas as pd


#getting store data from the api/ domain
def get_store_data_from_api():
    response = requests.get('https://api.data.codeup.com/api/v1/stores')
    data = response.json()
    stores = pd.DataFrame(data['payload']['stores'])
    stores = pd.DataFrame(stores)
    return stores


# geting the data using a while loop
def get_items_data_from_api():
    domain = 'https://api.data.codeup.com'
    endpoint = '/api/v1/items'
    items = []
    while True:
        url = domain + endpoint
        response = requests.get(url)
        data = response.json()
        print(f'\rGetting page {data["payload"]["page"]} of {data["payload"]["max_page"]}: {url}', end='')
        items.extend(data['payload']['items'])
        endpoint = data['payload']['next_page']
        if endpoint is None:
            break
    items = pd.DataFrame(items)
    return items

#getting sales data from the api/ domain
### this code loops through pages of an api and produces a data frame and saves it to csv
#KEEP IN MIND WHILE LOOP IS INVOLVED.... REMEMBER BREAKER
def get_sales_data_from_api():
    domain = 'https://api.data.codeup.com'
    endpoint = '/api/v1/sales'
    sales = []
    while True:
        url = domain + endpoint
        response = requests.get(url)
        data = response.json()
        print(f'\rGetting page {data["payload"]["page"]} of {data["payload"]["max_page"]}: {url}', end='')
        sales.extend(data['payload']['sales'])
        endpoint = data['payload']['next_page']
        if endpoint is None:
            break
    sales = pd.DataFrame(sales)
    return sales

# get data stored in csv or get it from api
def get_stores_from_csv():
    if os.path.exists('stores.csv'):
        return pd.read_csv('stores.csv')
    df = get_store_data_from_api()
    df.to_csv('stores.csv', index=False)
    return df

# get data stored in csv or get it from api
def get_items_from_csv():
    if os.path.exists('items.csv'):
        return pd.read_csv('items.csv')
    df = get_items_data_from_api()
    df.to_csv('items.csv', index=False)
    return df

# get data stored in csv or get it from api
def get_sales_from_csv():
    if os.path.exists('sales.csv'):
        return pd.read_csv('sales.csv')
    df = get_sales_data_from_api()
    df.to_csv('sales.csv', index=False)
    return df

#get store data combined(store,sales and items)
def get_store_data_combo():
    sales = get_sales_from_csv()
    stores = get_stores_from_csv()
    items = get_items_from_csv()

    sales = sales.rename(columns={'store': 'store_id', 'item': 'item_id'})
    df = pd.merge(sales, stores, how='inner', left_on='store_id', right_on='store_id')
    df = pd.merge(df, items, how='inner', left_on='item_id', right_on='item_id')
    return df

# acquire opsd(Open Power Systems Data for Germany) data 
def acquire_opsd_data():
    if os.path.exists('opsd.csv'):
        return pd.read_csv('opsd.csv')
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    df.to_csv('opsd.csv', index=False)
    return df
from yahoofinancials import YahooFinancials
from datetime import datetime

import pandas as pd
import requests

class price_data_generator:
    
    def __init__(self):       
        self.today_date : str = datetime.now().strftime('%Y-%m-%d')
        self.start_date : str = '2015-09-01'
        self.fred_api_key : str = '5e38d9310966ac372dbcbaa0ad94cdfa'
        self.end_date : str = '2023-08-31'
        
        
    def get_prices(self,ticker) -> pd.DataFrame: 
        yahoo_financials = YahooFinancials(ticker)
        try:
            historical_stock_prices : dict = yahoo_financials.get_historical_price_data(self.start_date, self.end_date, 'daily')
        except TypeError:
            print('Invalid ticker, try again')
        price_data : list = historical_stock_prices[ticker]['prices']
        
        data : list = []
        for day in price_data:
            date : str = day['formatted_date']
            adj_close_px : float = day['adjclose']
            close_px : float = day['close']
            high_px : float = day['high']
            low_px : float = day['low']
            open_px : float = day['open']
            data.append([date,close_px,adj_close_px,high_px,low_px,open_px])
        columns = ['date','close_px','adj_close_px','high_px','low_px','open_px']
        renamed_columns = [f'{ticker}_'+i if i != 'date' else i for i in columns]
        price_data : pd.DataFrame = pd.DataFrame(data,columns = renamed_columns)
          
        return price_data.reset_index(drop = True)
    
    def get_fred_data(self,inst):
        url : str = 'https://api.stlouisfed.org/fred/series/observations'

        params : dict = {
            'series_id': inst,     
            'api_key': self.fred_api_key,
            'file_type': 'json',      
            'observation_start': self.start_date,  
            'observation_end': self.end_date,    
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
        else:
            print(f"Error: {response.status_code}")
        
        price_data = []
        for day in data['observations']:
            date : str = day['date']
            if day['value'] != '.':
                price : float = float(day['value'])
                price_data.append([date,price])
                
        data : pd.DataFrame = pd.DataFrame(price_data,columns = ['date',f'{inst}_price'])
    
        return data
        


    
    
    
            
            





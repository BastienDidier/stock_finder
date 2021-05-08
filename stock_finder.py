import nsepy as nse
import datetime
import urllib3 
import random 
import numpy as np 
import pandas as pd
import nsepy as nse
import datetime
from nsetools import Nse
import matplotlib.pyplot as plt
import json

nsel = Nse()
stock_list = nsel.get_stock_codes() 
stock_list= {v: k for k, v in stock_list.items()}
stock_list.pop('NAME OF COMPANY')
Today = datetime.datetime.now()
potential_stock_list = [] 
for company in stock_list:
	stock_data =  nse.get_history(symbol=stock_list[company], start=datetime.datetime(2019,11,1), end=datetime.datetime(2021,3,27))
	stock_data['200_MA'] = stock_data['Close'].rolling(window=200).mean()
	stock_data['150_MA'] = stock_data['Close'].rolling(window=150).mean()
	stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
	metrics = {}
	metrics['200 MA'] = stock_data['200_MA'][-1]
	metrics['150 MA'] = stock_data['150_MA'][-1]
	metrics['50 MA'] = stock_data['50_MA'][-1]
	metrics['200 MA_1mago'] = stock_data['200_MA'][-30]
	metrics['150 MA_1mago'] = stock_data['150_MA'][-30]
	metrics['200 MA_2mago'] = stock_data['200_MA'][-60]
	metrics['150 MA_2mago'] = stock_data['150_MA'][-60]
	metrics['52W_Low'] = stock_data['Close'][-252:].min()
	metrics['52W_High'] = stock_data['Close'][-252:].max()
	metrics['price'] = stock_data['Close'][-1]#Current Price is at least 30% above 52 week low (1.3*low_of_52week)
	metrics['Above_30%_low'] = metrics['52W_Low'] *1.3
	# Condition 7: Current Price is within 25% of 52 week high 
	metrics['Within_25%_high'] = metrics['52W_High']*0.7
	metrics['condition1'] = (metrics['price'] > metrics['200 MA']) & (metrics['price'] > metrics['150 MA'])
	metrics['condition2'] = metrics['150 MA'] > metrics['200 MA']
	#3 The 200-day moving average line is trending up for 1 month 
	metrics['condition3'] = metrics['200 MA'] > metrics['200 MA_1mago']
	metrics['condition4'] = (metrics['50 MA'] > metrics['200 MA']) & (metrics['50 MA'] > metrics['150 MA'])
	metrics['condition5'] = metrics['price'] > metrics['50 MA']
	#6 The current stock price is at least 30 percent above its 52-week low
	metrics['condition6'] = metrics['price'] > metrics['Above_30%_low']
	#7 The current stock price is within at least 25 percent of its 52-week high.
	metrics['condition7'] = metrics['price'] > metrics['Within_25%_high']

	check_condition = True
	for i in range(1, 8):
		if metrics['condition'+str(i)] == False:
			check_condition = False

	if check_condition:
		with open('result_stock_finder.txt', 'a') as json_file:
  			json_file.write(company)
		print("new potential stock detected : "+company)

print("stock_finder end success")



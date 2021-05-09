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
import os

first = True
filePath = "result_stock_finder.txt";
# As file at filePath is deleted now, so we should check if file exists or not not before deleting them
if os.path.exists(filePath):
    os.remove(filePath)
with open('result_stock_finder.txt', 'a') as json_file:
	json_file.write("[")
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
	enough_data = True
	if len(stock_data['200_MA']) > 60 and len(stock_data['150_MA']) > 60 and len(stock_data['50_MA']) > 1 and len(stock_data['Close']) > 252:
		enough_data = True
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
		conditions = []
		conditions.append((metrics['price'] > metrics['200 MA']) & (metrics['price'] > metrics['150 MA']))
		conditions.append(metrics['150 MA'] > metrics['200 MA'])
		conditions.append(metrics['200 MA'] > metrics['200 MA_1mago'])
		conditions.append((metrics['50 MA'] > metrics['200 MA']) & (metrics['50 MA'] > metrics['150 MA']))
		conditions.append(metrics['price'] > metrics['50 MA'])
		conditions.append(metrics['price'] > metrics['Above_30%_low'])
		conditions.append(metrics['price'] > metrics['Within_25%_high'])

		for index, item in enumerate(conditions):
			if item:
				metrics['condition'+str(index + 1)] = 1
			else : 
				metrics['condition'+str(index + 1)] = 0

		check_condition = True
		for i in range(1, 8):
			if metrics['condition'+str(i)] == False:
				check_condition = False

	else:
		print("not enough_data : "+company)
		enough_data = False
	
	if check_condition and enough_data:
		company_result = {
		"name" : company,
		"symbol": stock_list[company],
		"metrics": metrics 
		}
		with open('result_stock_finder.txt', 'a') as json_file:
			if first:
				json.dump(company_result, json_file)
				first = False
			else:
				json.dump(company_result, json_file)
				json_file.write(",")
		print("new potential stock detected : "+company)

print("stock_finder end success")
with open('result_stock_finder.txt', 'a') as json_file:
	json_file.write("{}]")



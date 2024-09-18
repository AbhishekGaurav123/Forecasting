# -*- coding: utf-8 -*-
"""
Spyder Editor

@author Abhishek Gaurav
"""
"""import libraries
The requests module allows you to send HTTP requests using Python.
pandas to create dataframe or analysis and visualization
JSON is used to work with json data"""

import requests 
import pandas as pd
import json
from datetime import datetime

#website url from where we are fetching data and headers dictionary to input some encoding values used by website 
url = "https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY"
headers={"accept-encoding" : "gzip, deflate, br",
        "accept-language" : "en-US,en;q=0.9",
        "referer" :"https://www.nseindia.com/option-chain",
        "user-agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

#.text to convert data into string
response=requests.get(url, headers=headers).text
data=json.loads(response)

#to access data on the basis of expiry 
exp_list= data['records']['expiryDates']
exp_date = exp_list[0]

"""created dictionary for CE and PE data seperately  because for expiry
 data of Pe and Ce will missing sometime and variable to iterarte """
ce={}
pe={}
n=0
m=0

"""Loop to find the all data of same expiry date and insert it into the dictionary"""
for i in data['records']['data']:    
    if i['expiryDate'] == exp_date:
        
        try:
            print("1")
            ce[n] = i['CE']
            n= n+1
            
        except:
            pass
        try:
            print("2")
            pe[m]=i['PE']
            m =m+1
            
        except:
            pass
"""using pandas dataframe to store dictionary data for analysis and trandposed
data for analysis purpose transpose is used for  writing rows as columns"""
ce_df=pd.DataFrame.from_dict(ce).transpose()
ce_df.columns +="_CE_"
pe_df=pd.DataFrame.from_dict(pe).transpose()
pe_df.columns +="_PE_"

dataframe =pd.concat([ce_df, pe_df], join='inner' ,axis=1)

useful_data= dataframe[["openInterest_CE_", "changeinOpenInterest_CE_", 
                      "impliedVolatility_CE_",
                      "strikePrice_PE_", "impliedVolatility_PE_", 
                      "changeinOpenInterest_PE_",
                      "openInterest_PE_"]]
sum_Iv_CE=0
for j in useful_data['impliedVolatility_CE_']:
    sum_Iv_CE +=j
print("sum of Implied Volatility in CE: ", sum_Iv_CE)
    
sum_Iv_PE=0
for k in useful_data['impliedVolatility_PE_']:
    sum_Iv_PE +=k
print("sum of Implied Volatility in PE : ", sum_Iv_PE)

PCIVR=sum_Iv_PE/sum_Iv_CE


now = datetime.now()
current_time = now.strftime("%H:%M:%S")


list=[]
list.append(PCIVR)
print(list)


sum_coi_CE=0
for j in useful_data['changeinOpenInterest_CE_']:
    sum_coi_CE +=j
print("sum of Change of open interest in CE: ", sum_coi_CE)
    
sum_coi_PE=0
for k in useful_data['changeinOpenInterest_PE_']:
    sum_coi_PE +=k
print("sum of Change of open interest in PE : ", sum_coi_PE)

PCR=sum_coi_PE/sum_coi_CE

print("PCR  is", PCR , "at Time ", current_time)

print("PCIVR  is", PCIVR , "at Time ", current_time)
list.append(PCR)
list.append(current_time)
print(list)
    
position=0
insert_list=[]
for i in range(len(list)):
    insert_list.insert(i + position, list[i])
print(insert_list)

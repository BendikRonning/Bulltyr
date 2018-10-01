import pandas as pd


Bitcoin = pd.read_excel("Bitcoin.xlsx",sheet_name="Data")
Ripple = pd.read_excel("Ripple.xlsx",sheet_name="Data")
Ethereum = pd.read_excel("Ethereum.xlsx",sheet_name="Data")
Litecoin = pd.read_excel("Litecoin.xlsx",sheet_name="Data")
BitcoinCash = pd.read_excel("BitcoinCash.xlsx",sheet_name="Data")

Bitcoin["Change"] = Bitcoin["Close"].pct_change()
Ripple["Change"] = Ripple["Close"].pct_change()
Ethereum["Change"] = Ethereum["Close"].pct_change()
Litecoin["Change"] = Litecoin["Close"].pct_change()
BitcoinCash["Change"] = BitcoinCash["Close"].pct_change()

#SLÅR SAMMEN TIL EN DATAFRAME
frames = [Bitcoin, Ripple,Ethereum,Litecoin,BitcoinCash]
cryptoer = pd.concat(frames)

from Mappinger import days,months,season,weekend
import datetime as dt

cryptoer['Day of week'] = cryptoer['Date'].dt.dayofweek
cryptoer['Week number'] = cryptoer['Date'].dt.week
cryptoer['Month'] = cryptoer['Date'].dt.month
cryptoer['Year'] = cryptoer['Date'].dt.year
cryptoer['Time of week'] = cryptoer['Day of week'].apply(lambda x: weekend[x])
cryptoer['Day of week'] = cryptoer['Day of week'].apply(lambda x: days[x])
cryptoer['Season'] = cryptoer['Month'].apply(lambda x: season[x])
cryptoer['Month'] = cryptoer['Month'].apply(lambda x: months[x])
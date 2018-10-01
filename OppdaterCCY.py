import fix_yahoo_finance as yf
import pandas_datareader as pdr
import datetime
import numpy as np
import pandas as pd

start = datetime.datetime(2012,5,31)
end = datetime.datetime(2018,12,12)


bitcoin = ["BTC-USD"]
ripple = ["XRP-USD"]
ethereum = ["ETH-USD"]
litecoin = ["LTC-USD"]
bitcoincash = ["BCH-USD"]


dfBitcoin = yf.download(bitcoin, start=start, end=end)
dfRipple = yf.download(ripple, start=start, end=end)
dfEthereum = yf.download(ethereum, start=start, end=end)
dfLitecoin = yf.download(litecoin, start=start, end=end)
dfBitcoinCash = yf.download(bitcoincash, start=start, end=end)

dfBitcoin["Instrument"] = "Bitcoin"
dfRipple["Instrument"] = "Ripple"
dfEthereum["Instrument"] = "Ethereum"
dfLitecoin["Instrument"] = "Litecoin"
dfBitcoinCash["Instrument"] = "BitcoinCash"

dfBitcoin.to_excel("Bitcoin.xlsx",'Data')
dfRipple.to_excel("Ripple.xlsx",'Data')
dfEthereum.to_excel("Ethereum.xlsx",'Data')
dfLitecoin.to_excel("Litecoin.xlsx",'Data')
dfBitcoinCash.to_excel("BitcoinCash.xlsx",'Data')
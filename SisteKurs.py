from FellesCryptoData import cryptoer
import Ordbok

["Bitcoin","Bitcoin Cash","Ethereum", "Litecoin","Ripple"]

Navn = list(cryptoer.columns.values)

print(Navn)

SisteBitcoin= round(cryptoer["CLOSE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[0]].iloc[-1],2)
SisteBitcoinCash= round(cryptoer["CLOSE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[1]].iloc[-1],2)
SisteEthereum= round(cryptoer["CLOSE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[2]].iloc[-1],2)
SisteLitecoin= round(cryptoer["CLOSE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[3]].iloc[-1],2)
SisteRipple= round(cryptoer["CLOSE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[4]].iloc[-1],2)

ChangeBitcoin = round((cryptoer["CHANGE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[0]].iloc[-1])*100,2)
ChangeBitcoinC = round((cryptoer["CHANGE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[1]].iloc[-1])*100,2)
ChangeEthereum = round((cryptoer["CHANGE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[2]].iloc[-1])*100,2)
ChangeLitecoin = round((cryptoer["CHANGE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[3]].iloc[-1])*100,2)
ChangeRipple = round((cryptoer["CHANGE"].loc[cryptoer['INSTRUMENT'] == Ordbok.CryptoListe2[4]].iloc[-1])*100,3)

BitcoinLastTweet = str(Ordbok.CryptoListe[0])+": "+str(SisteBitcoin)+" USD ("+str(ChangeBitcoin)+"%)"
BitcoinCLastTweet = str(Ordbok.CryptoListe[1])+": "+str(SisteBitcoinCash)+" USD ("+str(ChangeBitcoinC)+"%)"
EthereumLastTweet = str(Ordbok.CryptoListe[2])+": "+str(SisteEthereum)+" USD ("+str(ChangeEthereum)+"%)"
LitecoinLastTweet = str(Ordbok.CryptoListe[3])+": "+str(SisteLitecoin)+" USD ("+str(ChangeLitecoin)+"%)"
RippleLastTweet = str(Ordbok.CryptoListe[4])+": "+str(SisteRipple)+" USD ("+str(ChangeRipple)+"%)"
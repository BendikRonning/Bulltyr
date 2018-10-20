from FellesCryptoData import cryptoer, Bitcoin, Ripple
import seaborn as sns
import matplotlib.pyplot as plt
import Ordbok

print(list(cryptoer.columns.values))
######################
######   PLOTS  ######
######################

Antall = len(Ripple)

x = cryptoer["CHANGE"].loc[cryptoer['INSTRUMENT'] == "Bitcoin"].tail(Antall)
y = cryptoer["CHANGE"].loc[cryptoer['INSTRUMENT'] == "Ripple"].tail(Antall)

Year2018 = cryptoer.loc[cryptoer['YEAR'] == 2018]
Year2018Sept = Year2018.loc[Year2018['MONTH'] == "Oct"]

StandardDev = Year2018Sept.groupby(["INSTRUMENT"]).std()
StandardDev["Standard deviation"] = StandardDev["CHANGE"]
StandardDev["Standard deviation"] = StandardDev["CHANGE"]*100

StandardDevList = StandardDev["Standard deviation"].tolist()
StandardDevList = [ '%.2f' % elem for elem in StandardDevList ]

BitcoinSTD = StandardDevList[0]
BitcoinCashSTD = StandardDevList[1]
EthereumSTD = StandardDevList[2]
LitecoinSTD = StandardDevList[3]
RippleSTD = StandardDevList[4]

print(Ordbok.CryptoListe[4]+" had a daily standard deviation of "+StandardDevList[4]+" percent")

SisteMND = sns.stripplot(x="INSTRUMENT",y="CHANGE",data=Year2018Sept,jitter=True,dodge=True)



plt.show()
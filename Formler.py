import pandas as pd
import numpy as np


def kalkuler_rsi(pris, n=14):
    delta = (pris-pris.shift(1)).fillna(0)
    avg_of_gains = delta[1:n+1][delta > 0].sum() / n
    avg_of_losses = -delta[1:n+1][delta < 0].sum() / n
    rsi_series = pd.Series(0.0, delta.index)
    up = lambda x: x if x > 0 else 0
    down = lambda x: -x if x < 0 else 0
    i = n+1
    for d in delta[n+1:]:
        avg_of_gains = ((avg_of_gains * (n-1)) + up(d)) / n
        avg_of_losses = ((avg_of_losses * (n-1)) + down(d)) / n
        if avg_of_losses != 0:
            rs = avg_of_gains / avg_of_losses
            rsi_series[i] = 100 - (100 / (1 + rs))
        else:
            rsi_series[i] = 100
        i += 1
    return rsi_series

def Støtte_og_Motstand(df):
    PP = pd.Series((df['HIGH'] + df['LOW'] + df['CLOSE']) / 3)
    R1 = pd.Series(2 * PP - df['LOW'])
    S1 = pd.Series(2 * PP - df['HIGH'])
    R2 = pd.Series(PP + df['HIGH'] - df['LOW'])
    S2 = pd.Series(PP - df['HIGH'] + df['LOW'])
    R3 = pd.Series(df['HIGH'] + 2 * (PP - df['LOW']))
    S3 = pd.Series(df['LOW'] - 2 * (df['HIGH'] - PP))
    psr = {'Pivot points':PP, 'First resistance':R1, 'First support':S1, 'Second resistance':R2, 'Second support':S2, 'Third resistance':R3, 'Third support':S3}
    PSR = pd.DataFrame(psr)
    df = df.join(PSR)
    return df

def Cryptoinfo(df):
    Kurs = df["CLOSE"].iloc[-1]
    Endring = df["Endring pris"].iloc[-1]
    Krypto = df["INSTRUMENT"].iloc[-1]
    Volume = df["VOLUME"].iloc[-1]
    return {"Kurs":Kurs,"Endring":Endring,"Krypto":Krypto,"Volume":Volume}
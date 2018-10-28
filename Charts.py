import pandas as pd
from FellesCryptoData import cryptoer
import numpy as np
from Formler import Støtte_og_Motstand, kalkuler_rsi,Cryptoinfo
import random
import seaborn as sns
import matplotlib.pyplot as plt
import Ordbok
from scipy.misc import imread
import matplotlib.cbook as cbook

df = cryptoer
df= df.rename(index=str, columns={"DATE": "Date"})
df= df.rename(index=str, columns={"CHANGE": "Endring pris"})

columnames = ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'ADJ CLOSE', 'VOLUME', 'INSTRUMENT', 'CHANGE', 'DAY OF WEEK', 'WEEK NUMBER', 'MONTH', 'YEAR', 'TIME OF WEEK', 'SEASON']

## KALKULERER NYE VARIABLER:


df_ripple = df.loc[df['INSTRUMENT'] == "Ripple"]
df_bitcoin = df.loc[df['INSTRUMENT'] == "Bitcoin"]
df_bitcoincash = df.loc[df['INSTRUMENT'] == "BitcoinCash"]
df_litecoin = df.loc[df['INSTRUMENT'] == "Litecoin"]
df_ethereum = df.loc[df['INSTRUMENT'] == "Ethereum"]

RandomCurrency = [df_ripple,df_bitcoin,df_bitcoincash,df_bitcoincash,df_litecoin,df_ethereum]

bilde_Logo = 'C:\\Users\\bendi\\OneDrive\\Pictures\\New folder\\Untitled.png'

dfAlldata = df

sistekurs = str(df["CLOSE"].iloc[-1])

def candlestick(df,daysinchart):
    from math import pi
    from bokeh.plotting import figure, show, output_file

    df = df.tail(daysinchart)

    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
    change_since_yesterday = round((df["Endring pris"].iloc[-1])*100,4)
    kurs = df["CLOSE"].iloc[-1]

    inc = df["CLOSE"] > df["OPEN"]
    dec = df["OPEN"] > df["CLOSE"]
    w = 12 * 60 * 60 * 1000  # Halv dag i mikrosekunder

    x = df["Date"]
    y = df["CLOSE"]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title=str(Selskapsnavn)+" - Candlestick - Siste kurs: "+str(kurs)+"(Change: "+str(change_since_yesterday)+"%)")
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.3
    p.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet
    p.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.1)  # legger til logo

    p.segment(df["Date"], df["HIGH"], df["Date"], df["LOW"], color="black")
    p.vbar(df["Date"][inc], w, df["OPEN"][inc], df["CLOSE"][inc], fill_color="green", line_color="black")
    p.vbar(df["Date"][dec], w, df["OPEN"][dec], df["CLOSE"][dec], fill_color="#F2583E", line_color="black")

    output_file("candlestick.html", title="candlestick.py example")

    show(p)  # open a browser

def candlestick_med_SMA(df,daysinchart,daysmovingaverage):
    from math import pi
    from bokeh.plotting import figure, show, output_file

    df[str(daysmovingaverage) + " days Exponential Moving Average"] = df["CLOSE"].rolling(window=daysmovingaverage).mean()
    df = df.tail(daysinchart)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])

    inc = df["CLOSE"] > df["OPEN"]
    dec = df["OPEN"] > df["CLOSE"]
    w = 12 * 60 * 60 * 1000  # Halv dag i mikrosekunder

    x = df["Date"]
    y = df["CLOSE"]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title=str(Selskapsnavn)+" - Candlestick - Siste kurs: "+str(sistekurs))
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.3
    p.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet
    p.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.3)  # legger til logo

    p.segment(df["Date"], df["HIGH"], df["Date"], df["LOW"], color="black")
    p.vbar(df["Date"][inc], w, df["OPEN"][inc], df["CLOSE"][inc], fill_color="green", line_color="black")
    p.vbar(df["Date"][dec], w, df["OPEN"][dec], df["CLOSE"][dec], fill_color="#F2583E", line_color="black")
    p.line(x=df["Date"], y=df[str(daysmovingaverage)+" days Exponential Moving Average"], line_color="black", line_width=5, legend=str(daysmovingaverage)+" days Exponential Moving Average")

    output_file("candlestick.html", title="candlestick.py example")

    show(p)  # open a browser

def candlestick_med_Støtte_Og_Motstand():
    from math import pi
    from bokeh.plotting import figure, show, output_file
    from bokeh.models import BoxAnnotation

    inc = df["CLOSE"] > df["OPEN"]
    dec = df["OPEN"] > df["CLOSE"]
    w = 12 * 60 * 60 * 1000  # Halv dag i mikrosekunder

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000,
               title=str(Selskapsnavn[0]) + " - Candlestick - Siste kurs: " + str(sistekurs))
    p.xaxis.major_label_orientation = pi / 4
    p.grid.grid_line_alpha = 0.3
    p.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet

    p.segment(df["Date"], df["HIGH"], df["Date"], df["LOW"], color="black")
    p.vbar(df["Date"][inc], w, df["OPEN"][inc], df["CLOSE"][inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df["Date"][dec], w, df["OPEN"][dec], df["CLOSE"][dec], fill_color="#F2583E", line_color="black")

    UnnaForsteStotte = round(((1-(df["First support"].iloc[-1]/df["CLOSE"].iloc[-1]))*100),2)

    p.line(x=df["Date"], y=df["Second resistance"].iloc[-1], line_color="black", line_width=3,
           legend="First restistance at "+str((round(df["First resistance"].iloc[-1],3))))
    p.line(x=df["Date"], y=df["Third resistance"].iloc[-1], line_color="black", line_width=3,
           legend="Second restistance at " + str((round(df["Second resistance"].iloc[-1], 3))))
    p.line(x=df["Date"], y=df["Third support"].iloc[-1], line_color="green", line_width=3,
           legend="First support at " + str((round(df["Second support"].iloc[-1],3))))
    p.line(x=df["Date"], y=df["Second support"].iloc[-1], line_color="green", line_width=3,
           legend="Second support at " + str((round(df["Third support"].iloc[-1],3))))

    low_box = BoxAnnotation(top=df["Second support"].iloc[-1],bottom=df["Third support"].iloc[-1], fill_alpha=0.2, fill_color='black')
    high_box = BoxAnnotation(top=df["Second resistance"].iloc[-1], bottom=df["Third resistance"].iloc[-1], fill_alpha=0.2,fill_color='black')

    p.add_layout(low_box)
    p.add_layout(high_box)

    output_file("candlestick.html", title="candlestick.py example")

    show(p)

def pos_vs_neg_volume():
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import Range1d, PanTool, ResetTool, HoverTool,LogColorMapper, LogTicker,ColorBar,SingleIntervalTicker

    ## Lager variabler

    xOpp = dfOpp["Date"].tail(200)
    yOpp = (dfOpp["VOLUME"].tail(200)*dfOpp["CLOSE"].tail(200))/1000000

    xNed = dfNed["Date"].tail(200)
    yNed = (dfNed["VOLUME"].tail(200) * dfNed["CLOSE"].tail(200)) / 1000000

    # Lager en output fil
    output_file("candlestick.html")

    ##Lager figur
    f = figure(x_axis_type="datetime",plot_width=1080)

    ## TOOLS

    f.tools = [PanTool(), ResetTool()]
    # f.add_tools(HoverTool()) #Legger til tool som gjør at vi kan ta musa over og se på punktene
    f.toolbar_location = "right"
    f.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet

    ## Styler tittelen på plottet

    f.title.text = str(Selskapsnavn[0])+" - Volume in NOK (MIO)"
    f.title.text_color = "black"
    f.title.text_font = "times"
    f.title.text_font_size = "20px"
    f.title.align = "center"

    ## Styler axelinjene

    f.xaxis.axis_label = "Date"
    f.yaxis.axis_label = "Volume in currency (MIO)"
    f.axis.axis_label_text_color = "black"  # farger navnene på labelsene
    f.axis.major_label_text_color = "black"  # farger verdiene på x og y aksen
    f.line(x=xOpp, y=medianVolumeOpp, line_color="green", line_width=5, legend="Median 90 positive days volume: "+str(medianVolumeOpp)+"MUSD")
    f.line(x=xNed, y=medianVolumeNed, line_color="red", line_width=5, legend="Median 90 negative days volume"+str(medianVolumeNed)+"MUSD")

    color_mapper = LogColorMapper(palette="PuBu7", low=400, high=1800)
    color_bar = ColorBar(color_mapper=color_mapper,
                         label_standoff=0, border_line_color=None, location=(0, 0))
    f.add_layout(color_bar, 'right')

    cr = f.circle(xOpp, yOpp, size=10,
                  fill_color="green",
                  fill_alpha=1, hover_alpha=1,
                  line_color=None, hover_line_color="green")
    cr2 = f.circle(xNed, yNed, size=10,
                  fill_color="red",
                  fill_alpha=1, hover_alpha=1,
                  line_color=None, hover_line_color="red")
    f.add_tools(HoverTool(tooltips=None, renderers=[cr,cr2], mode="hline"))


    ## Style gridden

    f.xgrid.grid_line_color = "gray"  # styler gridden
    f.grid.grid_line_dash = [5, 3]  # lager gridden stiplete

    ## Lager linje/scatter
    f.circle(xOpp, yOpp)  # Lager linjegraf

    show(f)

def volumline(df,daysinchart):
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import Range1d, PanTool, ResetTool, HoverTool,LogColorMapper, LogTicker,ColorBar,SingleIntervalTicker

    df = df.tail(daysinchart)

    ## Lager variabler
    x = df["Date"]
    y = (df["VOLUME"]*df["CLOSE"])/1000000

    medianVolume = ((df["VOLUME"].median()) * (df["CLOSE"].median())) / 1000000

    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])

    # Lager en output fil
    output_file("candlestick.html")

    ##Lager figur
    f = figure(x_axis_type="datetime",plot_width=1080)

    ## TOOLS

    f.tools = [PanTool(), ResetTool()]
    # f.add_tools(HoverTool()) #Legger til tool som gjør at vi kan ta musa over og se på punktene
    f.toolbar_location = "right"
    f.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet

    ## Styler tittelen på plottet

    f.title.text = str(Selskapsnavn)+" - Volume in USD"
    f.title.text_color = "black"
    f.title.text_font = "times"
    f.title.text_font_size = "20px"
    f.title.align = "center"

    ## Styler axelinjene

    f.xaxis.axis_label = "Date"
    f.yaxis.axis_label = "Volume in currency (MIO)"
    f.axis.axis_label_text_color = "black"  # farger navnene på labelsene
    f.axis.major_label_text_color = "black"  # farger verdiene på x og y aksen
    f.line(x=x, y=medianVolume, line_color="red", line_width=5, legend="Median "+str(daysinchart)+" days volume")

    color_mapper = LogColorMapper(palette="PuBu7", low=400, high=1800)
    color_bar = ColorBar(color_mapper=color_mapper,
                         label_standoff=0, border_line_color=None, location=(0, 0))
    f.add_layout(color_bar, 'right')

    cr = f.circle(x, y, size=10,
                  fill_color="black",
                  fill_alpha=1, hover_alpha=1,
                  line_color=None, hover_line_color="red")
    f.add_tools(HoverTool(tooltips=None, renderers=[cr], mode="hline"))


    ## Style gridden

    f.xgrid.visible = False  # Fjerner Gridlines
    f.ygrid.visible = False  # Fjerner Gridlines

    f.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.2)  # legger til logo

    ## Lager linje/scatter
    f.circle(x, y)  # Lager linjegraf

    show(f)

def scatterplot(df,daysinchart):
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import BoxAnnotation

    x = df["Date"].tail(daysinchart)
    y = df["Endring pris"].tail(daysinchart)*100

    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
    StdAvvik = round(df["Endring pris"].std()*100,2)

    TOOLS = "pan,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,tap,save,box_select,poly_select,lasso_select,"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title=str(Selskapsnavn)+" - Daily Ccanges - Standard deviation: "+str(StdAvvik)+" percent")
    p.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet

    p.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.2)  # legger til logo

    low_box = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='red')
    high_box = BoxAnnotation(bottom=0, fill_alpha=0.1, fill_color='green')

    p.add_layout(low_box)
    p.add_layout(high_box)

    p.scatter(x, y,
              fill_color="black", fill_alpha=0.8,
              line_color=None,size=8)

    output_file("candlestick.html", title="color_scatter.py example")

    show(p)

def MACD_BULLBEAR(df,daysinchart):
    from bokeh.plotting import figure, output_file, show

    from bokeh.io import show
    from bokeh.models import BoxAnnotation, Label
    from bokeh.plotting import figure

    df["12 Day Exponential Moving Average"] = df["CLOSE"].rolling(window=12).mean()
    df["26 Day Exponential Moving Average"] = df["CLOSE"].rolling(window=26).mean()
    df["MACD"] = df["12 Day Exponential Moving Average"] - df["26 Day Exponential Moving Average"]
    df["MACD Signal Line"] = df["MACD"].rolling(window=9).mean()
    df["Buy/Sell"] = df['MACD'] - df['MACD Signal Line']
    df["Zero"] = 0
    df["Sell"] = df[["Buy/Sell", "Zero"]].max(axis=1)
    df["Sell"] = df["Sell"].replace(0, np.nan)
    df["Buy"] = df[["Buy/Sell", "Zero"]].min(axis=1)
    df["Buy"] = df["Buy"].replace(0, np.nan)

    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])

    x = df["Date"].tail(daysinchart)
    y = df["MACD"].tail(daysinchart)
    d = df["MACD Signal Line"].tail(daysinchart)
    b = df["Buy/Sell"].tail(daysinchart)

    o = figure(plot_width=1000, plot_height=400,
               x_axis_type="datetime",title=str(Selskapsnavn)+" - MACD ANALYSE")

    o.line(x, y, color="black")
    o.line(x, 0, color="red",line_width=5)
    o.line(x, d, color="blue", line_width=5)

    low_box = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='red')
    high_box = BoxAnnotation(bottom=0, fill_alpha=0.1, fill_color='green')

    o.add_layout(low_box)
    o.add_layout(high_box)

    lables = Label(x=x.min(), y=y.max(), x_units='screen', text='Some Stuff', render_mode='css',
          border_line_color='black', border_line_alpha=1.0,
          background_fill_color='white', background_fill_alpha=1.0)

    o.add_layout(lables)

    o.image_url(url=[bilde_Logo], x=x.max()-((x.max()-x.min())/2), y=y.max()-((y.max()-y.min())/2), w=x.max()-x.min(), h=y.max()-y.min(), anchor='center', alpha=0.2) #legger til logo

    output_file("candlestick.html", title="color_scatter.py example")

    show(o)

def RSI(df,n):
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import BoxAnnotation
    from Formler import kalkuler_rsi

    df["RSI"] = kalkuler_rsi(df["CLOSE"])
    x = df["Date"].tail(n)
    y = df["RSI"].tail(n)

    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
    RSI_now = round(df["RSI"].iloc[-1],3)

    p = figure(plot_width=1000,plot_height=400,x_axis_type="datetime",title=str(Selskapsnavn)+" - RSI "+str(RSI_now))
    p.line(x, y, line_color="black", line_width=3, legend="14-Day RSI")
    p.line(x, 30, line_color="green", line_width=3, legend="Oversold")
    p.line(x, 70, line_color="red", line_width=3, legend="Overbought")
    p.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet
    p.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.3)  # legger til logo
    p.xgrid.visible = False #Fjerner Gridlines
    p.ygrid.visible = False #Fjerner Gridlines

    output_file("candlestick.html", title="color_scatter.py example")

    show(p)

def volume_alle(df,year):
    import seaborn as sns
    import matplotlib.pyplot as plt

    df = df.loc[df['YEAR'] == year]
    df = df.loc[df['VOLUME'] > 0]
    sns.stripplot(x="INSTRUMENT", y="VOLUME", data=df, jitter=True, dodge=True)
    plt.show()

def this_the_season():
    sns.stripplot(x="SEASON", y="Endring pris", data=df, jitter=True, hue="INSTRUMENT", dodge=True)
    plt.show()

def ready_for_the_weekend(df):
    sns.stripplot(x="TIME OF WEEK", y="Endring pris", data=df, jitter=True, hue="INSTRUMENT", dodge=True)
    plt.show()

sns.stripplot(x="YEAR",y="Endring pris",data=df,jitter=True,hue="INSTRUMENT",dodge=True)

img = imread("C:\\Users\\bendi\\OneDrive\\Pictures\\New folder\\Untitled.png")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.imshow(img,zorder=0,  extent=[0, 7, -2.0, 2.5])
plt.show()


plt.show()

##  UTVIKLING:

##  FERIDGE:
#MACD_BULLBEAR(df_ripple,100)
#scatterplot(df_ripple,500)
#volumline(df_ripple,90)
#candlestick(df_ripple,100)
#candlestick_med_SMA(df_ripple,100,40)
#RSI(df_ripple,100)

randomnumber = random.randint(0,len(RandomCurrency)-1)

df = Cryptoinfo(RandomCurrency[randomnumber])

print(df["Kurs"])
print(df["Endring"])
print(df["Krypto"])
print(df["Volume"])





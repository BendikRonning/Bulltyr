import pandas as pd
from FellesCryptoData import cryptoer
import numpy as np
df = cryptoer
df= df.rename(index=str, columns={"DATE": "Date"})
df= df.rename(index=str, columns={"CHANGE": "Endring pris"})

columnames = ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'ADJ CLOSE', 'VOLUME', 'INSTRUMENT', 'CHANGE', 'DAY OF WEEK', 'WEEK NUMBER', 'MONTH', 'YEAR', 'TIME OF WEEK', 'SEASON']

## KALKULERER NYE VARIABLER:

df["12 Day Exponential Moving Average"] = df["CLOSE"].rolling(window=12).mean()
df["26 Day Exponential Moving Average"] = df["CLOSE"].rolling(window=26).mean()
df["MACD"] = df["12 Day Exponential Moving Average"]-df["26 Day Exponential Moving Average"]
df["MACD Signal Line"] = df["MACD"].rolling(window=9).mean()
df["Buy/Sell"] = df['MACD']-df['MACD Signal Line']
df["Zero"] = 0
df["Sell"] = df[["Buy/Sell","Zero"]].max(axis=1)
df["Sell"] = df["Sell"].replace(0, np.nan)
df["Buy"] = df[["Buy/Sell","Zero"]].min(axis=1)
df["Buy"] = df["Buy"].replace(0, np.nan)


df_ripple = df.loc[df['INSTRUMENT'] == "Ripple"]
df_bitcoin = df.loc[df['INSTRUMENT'] == "Bitcoin"]
df_bitcoincash = df.loc[df['INSTRUMENT'] == "BitcoinCash"]
df_litecoin = df.loc[df['INSTRUMENT'] == "Litecoin"]
df_ethereum = df.loc[df['INSTRUMENT'] == "Ethereum"]

bilde_Logo = 'C:\\Users\\bendi\\OneDrive\\Pictures\\New folder\\Untitled.png'

dfAlldata = df

df = df.tail(90)
medianVolume = ((df["VOLUME"].median())*(df["CLOSE"].median()))/1000000

Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
sistekurs = str(df["CLOSE"].iloc[-1])

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

df["RSI"] = kalkuler_rsi(df["CLOSE"])

def candlestick_ripple():
    from math import pi
    from bokeh.plotting import figure, show, output_file

    df = df_ripple.tail(90)
    sistekurs = str(df["CLOSE"].iloc[-1])
    change_since_yesterday = round((df["Endring pris"].iloc[-1])*100,4)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])

    inc = df["CLOSE"] > df["OPEN"]
    dec = df["OPEN"] > df["CLOSE"]
    w = 12 * 60 * 60 * 1000  # Halv dag i mikrosekunder

    x = df["Date"]
    y = df["CLOSE"]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000,
               title=str(Selskapsnavn) + " - Candlestick - Siste kurs: " + str(sistekurs)+"("+str(change_since_yesterday)+"%)")
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

def candlestick_bitcoin():
    from math import pi
    from bokeh.plotting import figure, show, output_file

    df = df_bitcoin.tail(90)
    sistekurs = str(df["CLOSE"].iloc[-1])
    change_since_yesterday = round((df["Endring pris"].iloc[-1])*100,4)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])

    inc = df["CLOSE"] > df["OPEN"]
    dec = df["OPEN"] > df["CLOSE"]
    w = 12 * 60 * 60 * 1000  # Halv dag i mikrosekunder

    x = df["Date"]
    y = df["CLOSE"]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000,
               title=str(Selskapsnavn) + " - Candlestick - Siste kurs: " + str(sistekurs)+"("+str(change_since_yesterday)+"%)")
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

def candlestick_bitcoincash():
    from math import pi
    from bokeh.plotting import figure, show, output_file

    df = df_bitcoincash.tail(90)
    sistekurs = str(df["CLOSE"].iloc[-1])
    change_since_yesterday = round((df["Endring pris"].iloc[-1])*100,4)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])

    inc = df["CLOSE"] > df["OPEN"]
    dec = df["OPEN"] > df["CLOSE"]
    w = 12 * 60 * 60 * 1000  # Halv dag i mikrosekunder

    x = df["Date"]
    y = df["CLOSE"]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000,
               title=str(Selskapsnavn) + " - Candlestick - Siste kurs: " + str(sistekurs)+"("+str(change_since_yesterday)+"%)")
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

def candlestick_litecoin():
    from math import pi
    from bokeh.plotting import figure, show, output_file

    df = df_litecoin.tail(90)
    sistekurs = str(df["CLOSE"].iloc[-1])
    change_since_yesterday = round((df["Endring pris"].iloc[-1])*100,4)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])

    inc = df["CLOSE"] > df["OPEN"]
    dec = df["OPEN"] > df["CLOSE"]
    w = 12 * 60 * 60 * 1000  # Halv dag i mikrosekunder

    x = df["Date"]
    y = df["CLOSE"]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000,
               title=str(Selskapsnavn) + " - Candlestick - Siste kurs: " + str(sistekurs)+"("+str(change_since_yesterday)+"%)")
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

def candlestick_ethereum():
    from math import pi
    from bokeh.plotting import figure, show, output_file

    df = df_ethereum.tail(90)
    sistekurs = str(df["CLOSE"].iloc[-1])
    change_since_yesterday = round((df["Endring pris"].iloc[-1])*100,4)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])

    inc = df["CLOSE"] > df["OPEN"]
    dec = df["OPEN"] > df["CLOSE"]
    w = 12 * 60 * 60 * 1000  # Halv dag i mikrosekunder

    x = df["Date"]
    y = df["CLOSE"]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000,
               title=str(Selskapsnavn) + " - Candlestick - Siste kurs: " + str(sistekurs)+"("+str(change_since_yesterday)+"%)")
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

def candlestick():
    from math import pi
    from bokeh.plotting import figure, show, output_file

    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
    change_since_yesterday = round((df["Endring pris"].iloc[-1])*100,4)
    kurs = int(df["CLOSE"].iloc[-1])

    inc = df["CLOSE"] > df["OPEN"]
    dec = df["OPEN"] > df["CLOSE"]
    w = 12 * 60 * 60 * 1000  # Halv dag i mikrosekunder

    x = df["Date"]
    y = df["CLOSE"]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title=str(Selskapsnavn)+" - Candlestick - Siste kurs: "+str(kurs)+"("+str(change_since_yesterday)+"%)")
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

def volumline_ripple():
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import Range1d, PanTool, ResetTool, HoverTool,LogColorMapper, LogTicker,ColorBar,SingleIntervalTicker

    df = df_ripple.tail(90)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
    medianVolume = ((df["VOLUME"].median())*(df["CLOSE"].median()))/1000000

    ## Lager variabler
    x = df["Date"]
    y = (df["VOLUME"]*df["CLOSE"])/1000000

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

    f.title.text = str(Selskapsnavn)+" - Volume in USD (MIO)"
    f.title.text_color = "black"
    f.title.text_font = "times"
    f.title.text_font_size = "20px"
    f.title.align = "center"

    ## Styler axelinjene

    f.xaxis.axis_label = "Date"
    f.yaxis.axis_label = "Volume in USD (MIO)"
    f.axis.axis_label_text_color = "black"  # farger navnene på labelsene
    f.axis.major_label_text_color = "black"  # farger verdiene på x og y aksen
    f.line(x=x, y=medianVolume, line_color="red", line_width=5, legend="Median 90 days volume")

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

    f.xgrid.grid_line_color = "gray"  # styler gridden
    f.grid.grid_line_dash = [5, 3]  # lager gridden stiplete

    f.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.2)  # legger til logo

    ## Lager linje/scatter
    f.circle(x, y)  # Lager linjegraf

    show(f)

def volumline_bitcoin():
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import Range1d, PanTool, ResetTool, HoverTool,LogColorMapper, LogTicker,ColorBar,SingleIntervalTicker

    df = df_bitcoin.tail(90)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
    medianVolume = ((df["VOLUME"].median())*(df["CLOSE"].median()))/1000000
    ## Lager variabler
    x = df["Date"]
    y = (df["VOLUME"]*df["CLOSE"])/1000000

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

    f.title.text = str(Selskapsnavn)+" - Volume in USD (MIO)"
    f.title.text_color = "black"
    f.title.text_font = "times"
    f.title.text_font_size = "20px"
    f.title.align = "center"

    ## Styler axelinjene

    f.xaxis.axis_label = "Date"
    f.yaxis.axis_label = "Volume in USD (MIO)"
    f.axis.axis_label_text_color = "black"  # farger navnene på labelsene
    f.axis.major_label_text_color = "black"  # farger verdiene på x og y aksen
    f.line(x=x, y=medianVolume, line_color="red", line_width=5, legend="Median 90 days volume")

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

    f.xgrid.grid_line_color = "gray"  # styler gridden
    f.grid.grid_line_dash = [5, 3]  # lager gridden stiplete

    f.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.2)  # legger til logo

    ## Lager linje/scatter
    f.circle(x, y)  # Lager linjegraf

    show(f)

def volumline_bitcoincash():
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import Range1d, PanTool, ResetTool, HoverTool,LogColorMapper, LogTicker,ColorBar,SingleIntervalTicker

    df = df_bitcoincash.tail(90)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
    medianVolume = ((df["VOLUME"].median())*(df["CLOSE"].median()))/1000000
    ## Lager variabler
    x = df["Date"]
    y = (df["VOLUME"]*df["CLOSE"])/1000000

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

    f.title.text = str(Selskapsnavn)+" - Volume in USD (MIO)"
    f.title.text_color = "black"
    f.title.text_font = "times"
    f.title.text_font_size = "20px"
    f.title.align = "center"

    ## Styler axelinjene

    f.xaxis.axis_label = "Date"
    f.yaxis.axis_label = "Volume in USD (MIO)"
    f.axis.axis_label_text_color = "black"  # farger navnene på labelsene
    f.axis.major_label_text_color = "black"  # farger verdiene på x og y aksen
    f.line(x=x, y=medianVolume, line_color="red", line_width=5, legend="Median 90 days volume")

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

    f.xgrid.grid_line_color = "gray"  # styler gridden
    f.grid.grid_line_dash = [5, 3]  # lager gridden stiplete

    f.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.2)  # legger til logo

    ## Lager linje/scatter
    f.circle(x, y)  # Lager linjegraf

    show(f)

def volumline_litecoin():
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import Range1d, PanTool, ResetTool, HoverTool,LogColorMapper, LogTicker,ColorBar,SingleIntervalTicker

    df = df_litecoin.tail(90)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
    medianVolume = ((df["VOLUME"].median())*(df["CLOSE"].median()))/1000000
    ## Lager variabler
    x = df["Date"]
    y = (df["VOLUME"]*df["CLOSE"])/1000000

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

    f.title.text = str(Selskapsnavn)+" - Volume in USD (MIO)"
    f.title.text_color = "black"
    f.title.text_font = "times"
    f.title.text_font_size = "20px"
    f.title.align = "center"

    ## Styler axelinjene

    f.xaxis.axis_label = "Date"
    f.yaxis.axis_label = "Volume in USD (MIO)"
    f.axis.axis_label_text_color = "black"  # farger navnene på labelsene
    f.axis.major_label_text_color = "black"  # farger verdiene på x og y aksen
    f.line(x=x, y=medianVolume, line_color="red", line_width=5, legend="Median 90 days volume")

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

    f.xgrid.grid_line_color = "gray"  # styler gridden
    f.grid.grid_line_dash = [5, 3]  # lager gridden stiplete

    f.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.2)  # legger til logo

    ## Lager linje/scatter
    f.circle(x, y)  # Lager linjegraf

    show(f)

def volumline_ethereum():
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import Range1d, PanTool, ResetTool, HoverTool,LogColorMapper, LogTicker,ColorBar,SingleIntervalTicker

    df = df_ethereum.tail(90)
    Selskapsnavn = str(df["INSTRUMENT"].iloc[-1])
    medianVolume = ((df["VOLUME"].median())*(df["CLOSE"].median()))/1000000
    ## Lager variabler
    x = df["Date"]
    y = (df["VOLUME"]*df["CLOSE"])/1000000

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

    f.title.text = str(Selskapsnavn)+" - Volume in USD (MIO)"
    f.title.text_color = "black"
    f.title.text_font = "times"
    f.title.text_font_size = "20px"
    f.title.align = "center"

    ## Styler axelinjene

    f.xaxis.axis_label = "Date"
    f.yaxis.axis_label = "Volume in USD (MIO)"
    f.axis.axis_label_text_color = "black"  # farger navnene på labelsene
    f.axis.major_label_text_color = "black"  # farger verdiene på x og y aksen
    f.line(x=x, y=medianVolume, line_color="red", line_width=5, legend="Median 90 days volume")

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

    f.xgrid.grid_line_color = "gray"  # styler gridden
    f.grid.grid_line_dash = [5, 3]  # lager gridden stiplete

    f.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.2)  # legger til logo

    ## Lager linje/scatter
    f.circle(x, y)  # Lager linjegraf

    show(f)

def volumline():
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import Range1d, PanTool, ResetTool, HoverTool,LogColorMapper, LogTicker,ColorBar,SingleIntervalTicker

    ## Lager variabler
    x = df["Date"]
    y = (df["VOLUME"]*df["CLOSE"])/1000000

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
    f.line(x=x, y=medianVolume, line_color="red", line_width=5, legend="Median 90 days volume")

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

    f.xgrid.grid_line_color = "gray"  # styler gridden
    f.grid.grid_line_dash = [5, 3]  # lager gridden stiplete

    f.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.2)  # legger til logo

    ## Lager linje/scatter
    f.circle(x, y)  # Lager linjegraf

    show(f)

def scatterplot():
    from bokeh.plotting import figure
    from bokeh.io import output_file, show, save
    from bokeh.models import Range1d, PanTool, ResetTool, HoverTool, LogColorMapper, LogTicker, ColorBar, SingleIntervalTicker

    x = dfAlldata["Date"]
    y = dfAlldata["Endring pris"]

    TOOLS = "pan,wheel_zoom,zoom_in,zoom_out,box_zoom,reset,tap,save,box_select,poly_select,lasso_select,"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, title=str(Selskapsnavn[0])+" - Daglige endringer - Siste kurs: "+str(sistekurs))
    p.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet

    p.image_url(url=[bilde_Logo], x=x.max() - ((x.max() - x.min()) / 2), y=y.max() - ((y.max() - y.min()) / 2),
                w=x.max() - x.min(), h=y.max() - y.min(), anchor='center', alpha=0.2)  # legger til logo

    p.scatter(x, y,
              fill_color="black", fill_alpha=0.8,
              line_color=None,size=8)

    output_file("candlestick.html", title="color_scatter.py example")

    show(p)

def MACD():
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import BoxAnnotation

    x = df["Date"]
    y = df["MACD"]
    d = df["MACD Signal Line"]



    o = figure(plot_width=1080,plot_height=400,x_axis_type="datetime",title=str(Selskapsnavn[0])+" - MACD ANALYSE")
    o.line(x, y, color="#FB8072")
    o.line(x, d, color="blue")

    low_box = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='red')
    high_box = BoxAnnotation(bottom=0, fill_alpha=0.1, fill_color='green')

    o.add_layout(low_box)
    o.add_layout(high_box)

    output_file("candlestick.html", title="color_scatter.py example")

    show(o)

def MACD_BULLBEAR():
    from bokeh.plotting import figure, output_file, show

    from bokeh.io import show
    from bokeh.models import BoxAnnotation, Label
    from bokeh.plotting import figure

    x = df["Date"]
    y = df["MACD"]
    d = df["MACD Signal Line"]
    b = df["Buy/Sell"]

    o = figure(plot_width=1000, plot_height=400,
               x_axis_type="datetime",title=str(Selskapsnavn)+" - MACD ANALYSE")

    o.line(x, y, color="black")
    o.line(x, 0, color="red",line_width=5)

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

def RSI():
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import BoxAnnotation

    x = dfAlldata["Date"].tail(200)
    y = dfAlldata["RSI"].tail(200)

    RSI_now = round(df["RSI"].iloc[-1],3)

    p = figure(plot_width=1000,plot_height=400,x_axis_type="datetime",title=str(Selskapsnavn[0])+" - RSI "+str(RSI_now))
    p.line(x, y, line_color="black", line_width=3, legend="14-Day RSI")
    p.line(x, 30, line_color="green", line_width=3, legend="Oversold")
    p.line(x, 70, line_color="red", line_width=3, legend="Overbought")
    p.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet


    output_file("candlestick.html", title="color_scatter.py example")

    show(p)
    
    
##  UTVIKLING:
candlestick_ripple()
volumline_ripple()

candlestick_bitcoin()
volumline_bitcoin()

candlestick_bitcoincash()
volumline_bitcoincash()

candlestick_litecoin()
volumline_litecoin()

candlestick_ethereum()
volumline_ethereum()

##  FERIDGE:
#MACD_BULLBEAR()
#scatterplot()
#volumline()
#MACD()
#candlestick()


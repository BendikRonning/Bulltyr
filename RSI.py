#RSI
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


def RSI():
    from bokeh.plotting import figure, output_file, show

    x = dfAlldata["Date"].tail(200)
    y = dfAlldata["RSI"].tail(200)


    p = figure(plot_width=1000,plot_height=400,x_axis_type="datetime",title=str(Selskapsnavn[0])+" - RSI ANALYSE")
    p.line(x, y, line_color="black", line_width=3, legend="14-Day RSI")
    p.toolbar.logo = None  # Fjerner Bokeh logoen fra chartet

    output_file("candlestick.html", title="color_scatter.py example")

    show(p)

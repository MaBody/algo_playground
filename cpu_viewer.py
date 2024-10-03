import dash
import pandas as pd
import numpy as np
import plotly.express as px
import psutil
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(filename="log_cpu.log",
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
load_list = []
time_list = []
x_lim = 10


def get_xlim():
    return x_lim


def set_xlim(val):
    x_lim = val


og_time = time.time()
labels = [f"core {i}" for i in range(1, 9)]

app = dash.Dash(__name__)
app.layout = dash.html.Div(
    children=[dash.html.H1(children="CPU Load", id="title", style={'textAlign': 'center'}),
              dash.dcc.Graph(id="cpu_load", animate=True),
              dash.dcc.Interval(id="interval", interval=2000)]
)


@app.callback(
    dash.Output("cpu_load", "figure"),
    dash.Input("interval", "n_intervals"),
)
def update_cpu_load(n_intervals: int):
    stamp = time.time() - og_time
    load = psutil.cpu_percent(interval=1, percpu=True)

    load_list.append(load)
    time_list.append(stamp)
    df = pd.DataFrame(load_list,
                      index=time_list,
                      columns=[f"core {i}" for i in range(1, 9)])
    df.index.name = "time (s)"
    h = get_xlim()
    while df.index[-1] > h:
        h *= 2
    set_xlim(h)
    # logger.log(logging.INFO, "{}, {}".format(load, load))
    # return px.line(x=time_list, y=load_list, range_x=x_lim, range_y=1)
    # return px.line(df, x=df.index, y=df.columns[1:], color=color, range_x=(0, get_xlim()))
    return px.line(df, x=df.index, y=df.columns, range_x=(0, h), range_y=(0, 100))


if __name__ == "__main__":
    app.run()

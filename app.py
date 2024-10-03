# %%
import multiprocessing as mp
import numpy as np
import psutil
import argparse
import logging

# from dash import Dash, html, dcc, callback, Output, Input
import dash
import plotly.express as px
import pandas as pd
import reduce

# print(mp.cpu_count())
# print(psutil.cpu_percent())
# print(psutil.cpu_times_percent())
# %%

parser = argparse.ArgumentParser("Simulation of parallel reduction.")
# Required positional argument
parser.add_argument('n', type=int,
                    help='The size of the problem instance.')

# Optional positional argument
parser.add_argument('p', type=int,
                    help='The number of processing units.')

# get the multiprocessing logger
logger = mp.get_logger()
# configure a stream handler
logger.addHandler(logging.StreamHandler())
# log all messages, debug and up
logger.setLevel(logging.DEBUG)


def run_trials(n, p):
    # Trivial sum: n*(n+1)/2
    run_size = np.round(n/p)
    data = np.arange(n)
    np.random.shuffle(data)
    print("Successful!")
    visualize_output(data)


def visualize_output(data: np.ndarray):
    n = len(data)
    classes = np.arange(1, 5)
    app = dash.Dash(__name__)

    app.layout = [
        dash.html.H1(children='Class Selector', style={'textAlign': 'center'}),
        dash.dcc.Dropdown(classes, 1, id='dropdown', multi=True),
        dash.dcc.Graph(id='graph')
    ]

    @dash.callback(
        dash.Output('graph', 'figure'),
        dash.Input('dropdown', 'value')
    )
    def update_graph(value: int | list[int]):
        value = [value] if isinstance(value, int) else value
        value = ["{}".format(i) for i in value]
        labels = np.repeat(classes, np.ceil(n/len(classes)))[:n]
        assert n == len(labels), print(len(labels))
        df = pd.DataFrame({"x": data, "y": data, "label": labels.astype(str)})
        selection = df.query(f"label in {value}")
        fig = px.scatter(selection, "x", "y", color="label", range_x=(0, n), range_y=(0, n))
        return fig

    app.run(debug=True)


if __name__ == "__main__":
    args: argparse.Namespace = parser.parse_args()
    n, p = args.n, args.p
    output = run_trials(n, p)
    # visualize_output(output)

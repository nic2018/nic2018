#%%
import pandas as pd
import datetime
import plotly.graph_objs as go
from TF_Simple_Sig import TF_simple
from plotly.subplots import make_subplots

def trade_signal(data):
    data['date_time'] = [(datetime.datetime(1,1,1)+ datetime.timedelta(epoch_time)- datetime.timedelta(days=367)).strftime('%Y%m%d %H:%M:%S') for epoch_time in data['date']]
    # Create the figure with two subplots
    # top part is price chart with entry/exit signal
    # bottom part is accumulate return (equity) from running the TF_Simple model
    fig = make_subplots(rows = 2, cols= 1,shared_xaxes=True) #, specs=[[{'secondary_y': True}]])

    # create the price chart trace
    fig.add_trace(
                go.Scatter(x=data['date_time'],
                                y=data['ts2'],
                                mode='markers',
                                name='ts2'), row = 1, col = 1)            
    
    # create the scatter trace for buy/sell entry/exit signals
    # plot buy entry signal on the price series
    fig.add_trace(
                go.Scatter(x=data['date_time'],
                                y=data['b_sig'],
                                mode='markers',
                                marker=dict(color='blue', symbol='triangle-up'),
                                name='Buy Entry'), row = 1, col = 1)
    # plot buy exit signal on the price series
    fig.add_trace(
                go.Scatter(x=data['date_time'],
                                y=data['exit_b_sig'],
                                mode='markers',
                                marker=dict(color='blue', symbol='triangle-down'),
                                name='Buy Exit'), row = 1, col = 1)
    # plot buy entry signal on the price curve
    fig.add_trace(
                go.Scatter(x=data['date_time'],
                                y=data['s_sig'],
                                mode='markers',
                                marker=dict(color='#B82E2E', symbol='triangle-up'),
                                name='Sell Entry'), row = 1, col = 1)
    # plot sell exit signal on the price series
    fig.add_trace(
                go.Scatter(x=data['date_time'],
                                y=data['exit_s_sig'],
                                mode='markers',
                                marker=dict(color='#B82E2E', symbol='triangle-down'),
                                name='Sell Exit'), row = 1, col = 1)

    
    # calculate equity series
    data['cum_r']= 1+data['return'].cumsum()
    #data.iloc[0]['cum_r'] = 1 
    # plot equity series
    fig.add_trace(
                go.Scatter(x=data['date_time'],
                                y=data['cum_r'],
                                name='Equity'), row = 2, col = 1)
    
    fig.show()

# call trading model function to generate signals  
signals = TF_simple(2200, 450, 0.00025) #0.00001)
# call above trade_signal function to generate signal and equity curve
trade_signal(signals)

# %%

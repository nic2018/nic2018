#%%
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objs as go
from TF_Simple_Sig import TF_simple


def trade_equity(data):
    data['date_time'] = [(datetime.datetime(1,1,1)+ datetime.timedelta(epoch_time)- datetime.timedelta(days=367)).strftime('%Y%m%d %H:%M:%S') for epoch_time in data['date']]
    # check for missing data and count the number of missing values in each column
    data['date_time'] = pd.to_datetime(data['date_time'])
    # group data in year and count % missing value of each column 
    d_return = data.groupby(data['date_time'].dt.date).sum()
    # calculate equity series
    d_return['cum_r']= 1+d_return['return'].cumsum()
    #d_return.loc[0,'cum_r'] = 1 
    # clculate drawdown
    running_max = np.maximum.accumulate(d_return['cum_r'])
    d_return['dd'] = d_return['cum_r'] - running_max
    d_return.to_csv('simpleEQ.csv')
    
    fig = go.Figure()

    # plot equity series
    fig.add_trace(
                go.Scatter(x=d_return.index,
                                y=d_return['cum_r'],
                                name='Equity'))
    fig.add_trace(
            go.Bar(x=d_return.index,
                            y=d_return['dd'],
                            name='Drawdowm', yaxis= 'y2', opacity=0.6))
    fig.update_layout(title='Dialy Equity',
                      yaxis1=dict(title='Equity'),
                      yaxis2=dict(title='Drawdown', overlaying='y', side='right')) 

    fig.show()

# call trading model function to generate signals  
signals = TF_simple(2200, 450, 0.00025) #0.00001)

# call above trade_signal function to generate signal and equity curve
trade_equity(signals)

# %%
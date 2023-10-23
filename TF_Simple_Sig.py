# this module built a simple trading model (testing entry/exit lookback)
# Entry of long/short in ts2 is triggered when ts1 reach lowest/highest ts1 price of last long lookback (para1) periods,
# Exit of long/short in ts2 is triggered when ts1 reach highest/lowest ts1 price of last shortlookback (para2) periods

#%%  
import pandas as pd
import numpy as np
import datetime

def TF_simple(para1, para2, mincost):
    long_lb = para1
    short_lb = para2
    cost = mincost #0.00002
    # read the trading data into a pandas data frame
    df = pd.read_csv('quantTest_data.csv',header = None, names = ['date','ts1','ts2'])
    
    # calculate entry(price based on long lb) /exit(price based on short lb) point based on ts1
    df['lh'] = df['ts1'].rolling(long_lb, int(long_lb*0.06)).max().shift()  
    df['sh'] = df['ts1'].rolling(short_lb,int(short_lb*0.06)).max().shift() 
    df['ll'] = df['ts1'].rolling(long_lb,int(long_lb*0.06)).min().shift() 
    df['sl'] = df['ts1'].rolling(short_lb,int(short_lb*0.06)).min().shift() 

    # Initialize a position variable
    position = 0
    # Initialize total # of Trade variable
    num_trd = 0
    Pos = []
    df['b_sig'] = pd.Series()
    df['s_sig'] = pd.Series()
    df['exit_b_sig'] = pd.Series()  
    df['exit_s_sig'] = pd.Series()   
    # Loop over data to determine buy, sell, or hold
    # ts2 signal opposite to ts1  
    for i, row in df.iterrows():
        # Sell signal, ts1 buy = ts2 sell
        if position == 0 and row['ts1'] >= row['lh'] and row['sl'] != row['lh'] and row['ts2'] != None:
            row['s_sig'] = row['ts2']   
            row['ts2'] = row['ts2']-cost
            num_trd +=1
            position = -1
        # Exit sell signal
        elif position == -1 and row['ts1'] <= row['sl'] and row['ts2'] != None:
            row['exit_s_sig'] = row['ts2'] 
            row['ts2'] = row['ts2']+cost
            position = 0
        # Buy signal
        elif position == 0 and row['ts1'] <= row['ll'] and row['sh'] != row['ll'] and row['ts2'] != None:
            row['b_sig'] = row['ts2']   
            row['ts2'] = row['ts2']+cost
            num_trd +=1
            position= 1
        # Exit Buy signal
        elif position == 1 and row['ts1'] >= row['sh'] and row['ts2'] != None:
            row['exit_b_sig'] = row['ts2']   
            row['ts2'] = row['ts2']-cost
            position = 0
        Pos.append(position)


    df['position'] = Pos         
    # Count the total number of holding period 
    count = (df['position'] != 0).sum()
    # calculate averahe holding period per trade
    avglen = count/num_trd
    # drop null value in price series
    df = df.dropna(subset=['ts1', 'ts2'])
    # Calculate daily returns
    df['return'] = np.log(df['ts2'] / df['ts2'].shift(1)) * df['position'].shift(1)
    df['avg_len'] = avglen
    # create sig_df for return and signal series
    sig_df = df.loc[:, ['date','ts2','return', 'b_sig','exit_b_sig','s_sig','exit_s_sig','avg_len']]
    sig_df = sig_df.dropna(subset=['return'])
  
    return sig_df
    # sig_df.to_csv('sig.csv')

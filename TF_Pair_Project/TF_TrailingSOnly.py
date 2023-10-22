# this module built a simple trading model 
# Entry of long/short in ts2 is triggered when ts1 reach lowest/highest ts1 price of last long lookback (para1) periods,
# Exit condtion :
#    Trailing Stop Exit: when ts2 > (highest since entry - trail * volatility range) for long or ts2 > (lowest since entry + trail * volatility range) for short


#%%  
import pandas as pd
import numpy as np
import datetime


def TF_trailing(para1, para2, trail, vol_lb, mincost):
    long_lb = para1
    short_lb = para2
    cost = mincost #0.00002
    # read the trading data into a pandas data frame
    df = pd.read_csv('quantTest_data.csv',header = None, names = ['date','ts1','ts2'], index_col = 0)

    # calculate entry(price based on long lb) /exit(price based on short lb)  range based on ts1
    df['lh'] = df['ts1'].rolling(long_lb, int(long_lb*0.06)).max().shift() 
    #df['sh'] = df['ts1'].rolling(short_lb,int(short_lb*0.06)).max().shift() 
    df['ll'] = df['ts1'].rolling(long_lb,int(long_lb*0.06)).min().shift() 
    #df['sl'] = df['ts1'].rolling(short_lb,int(short_lb*0.06)).min().shift() 
    # Calculate a volatility range using last vol_lb period's highest high - lowest low for exit stretch calculation
    df['vol'] = df['ts2'].rolling(vol_lb,int(vol_lb*0.06)).max().shift() - df['ts2'].rolling(vol_lb,int(vol_lb*0.06)).min().shift() 
    # Forward fill null values in 'vol' column
    df['vol'] = df['vol'].fillna(method='ffill')
    # Initialize position variable and trailing price for exit
    position = 0
    num_trd = 0
    trailing_peak = 0
    trailing_stop = 0
    Pos = []
    # Define a function to determine whether to buy, sell, or hold
    # ts2 signal opposite to ts1  
    # Loop through the data and apply the trading strategy
    for i, row in df.iterrows():
        if row['vol'] != None :
            # Sell signal 
            # validate there is different between long entry (lh) and short entry (sl)
            # ts2 not null for entry
            if position == 0 and row['ts1'] >= row['lh'] and row['ll'] != row['lh'] and row['ts2'] != None:
                row['ts2'] = row['ts2']-cost
                num_trd+=1
                position = -1
                # initialized lowest price since entry for trailing exit
                trailing_peak = row['ts2']
                # validate high - low range, if range = 0 not appropriate for exit signal
                if row['vol'] != 0:
                    trailing_stop = trailing_peak + trail * row['vol']
                else:
                    trailing_stop = 0
            # Exit Sell signal
            elif position == -1:
                # ts2 not null for exit
                # validate trailing stop price is valid  
                if  (trailing_stop != 0 and row['ts2'] >= trailing_stop) :
                    row['ts2'] = row['ts2']+cost
                    position = 0                
                else:
                    # ts2 not null to update trailing peak 
                    if row['ts2'] != None:
                        trailing_peak = min(row['ts2'], trailing_peak) 
                    # validate volatility range not 0 
                    if row['vol'] != 0:    
                        trailing_stop = trailing_peak + trail * row['vol']  
                    else:
                        trailing_stop = 0
                            
            # Buy signal
            elif position == 0 and row['ts1'] <= row['ll'] and row['lh'] != row['ll'] and row['ts2'] != None :
                row['ts2'] = row['ts2']+cost
                num_trd+=1
                position= 1
                # initialized highest price since entry for trailing exit
                trailing_peak = row['ts2'] 
                if row['vol'] != 0:
                    trailing_stop = trailing_peak - trail * row['vol']
                else:
                    trailing_stop = 0          
            # Exit Buy signal
            elif position == 1:
                if (trailing_stop != 0 and row['ts2'] <= trailing_stop):
                    row['ts2'] = row['ts2']-cost
                    position = 0
                else:
                    if row['ts2'] != None:
                        trailing_peak = max(row['ts2'], trailing_peak) 
                    if row['vol'] != 0:
                        trailing_stop = trailing_peak - trail * row['vol']    
                    else:
                        trailing_stop = 0                       
        Pos.append(position)
    
    df['position'] = Pos
    df = df.dropna(subset=['ts1', 'ts2'])
    # Calculate daily returns
    df['return'] = np.log(df['ts2'] / df['ts2'].shift(1)) * df['position'].shift(1)

    # create sig_df for return series
    sig_df = df.loc[:, ['return']]
    sig_df['num_trd'] = num_trd

    return sig_df
    # sig_df.to_csv('sig.csv')

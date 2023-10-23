#%%
import numpy as np
import pandas as pd
import plotly.graph_objs as go

class Equity:
    def __init__(self, daily_returns):
        self.daily_returns = daily_returns

    def get_return(self):
        # calculate average return 
        self.mean_return = np.mean(self.daily_returns)
        return self.mean_return

    def get_sharpe(self):
        # calculate sharpe ratio
        self.mean_return = np.mean(self.daily_returns)
        self.std_dev = np.std(self.daily_returns)
        self.sharpe_ratio = self.mean_return / self.std_dev
        return self.sharpe_ratio

    def get_sortino(self):    
        # calculate Modified sortino ratio based on downside deviation
        self.mean_return = np.mean(self.daily_returns)
        downside_returns = self.daily_returns[self.daily_returns < 0]
        downside_std_dev = np.sqrt((downside_returns ** 2).sum()/self.daily_returns.count())
        self.sortino_ratio = self.mean_return / downside_std_dev
        return self.sortino_ratio
        
    def get_equity_series(self):
        # calculate accumulate equity 
        equity_curve = 1+self.daily_returns.cumsum()
        equity_curve.iloc[0]= 1        
        return equity_curve
    
    def drawdown(self):   
        # calculate continued drawdown
        equity_curve =  1+self.daily_returns.cumsum()
        equity_curve.iloc[0]= 1           
        #running_max1 = equity_curve.cummax()
        running_max = np.maximum.accumulate(equity_curve)
        drawdown = equity_curve - running_max
        return drawdown
    
    
    def get_maxdd(self):
        # calculate max drawdown
        maxdd = self.drawdown().min()
        return maxdd

    def get_maxdd_ratio(self):
        # calculate max drawdown ratio Avg Return/Max dd
        self.mean_return = np.mean(self.daily_returns)
        maxdd_ratio = self.mean_return/-self.drawdown().min()
        return self.mean_return,  self.drawdown().min(), maxdd_ratio 


    def plot_series(self):
        # plot equity curve and drawdown curve
        drawdown = self.drawdown()
        equity = self.get_equity_series()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=equity.index, y =equity, name="Equity"))
        fig.add_trace(go.Bar(x=drawdown.index,y=drawdown,marker=dict(color="dark gray"), name="Drawdown"))
        fig.show()  
    
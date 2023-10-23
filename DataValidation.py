# this data Validation module will check missing data and invalid data
# calculate some statistic number on Missing data 
# calculate simple correlation of the 1 period return
#%%  
import pandas as pd
import numpy as np
import datetime
import scipy.stats as stats
import plotly.graph_objects as go

# read the trading data into a pandas data frame
df = pd.read_csv('quantTest_data.csv',header = None, names = ['date','ts1','ts2'], index_col = 0)

# Convert date col to readarble date time
df['date_time'] = [(datetime.datetime(1,1,1)+ datetime.timedelta(epoch_time)- datetime.timedelta(days=367)).strftime('%Y%m%d %H:%M:%S') for epoch_time in df.index]
df['m_ts1'] = pd.Series()
df['m_ts2'] = pd.Series()
# check for missing data and count the number of missing values in each column
df[['m_ts1', 'm_ts2']]= df[['ts1', 'ts2']].isnull()
df['date_time'] = pd.to_datetime(df['date_time'])
# group data in year and count % missing value of each column 
yearly_data = df.groupby(df['date_time'].dt.year).mean()
# group data in hour and count % missing value of each column
hourly_data = df.groupby(df['date_time'].dt.hour).mean()

#print(yearly_data)
fig = go.Figure()
fig.add_trace(go.Bar(x = yearly_data.index, y =yearly_data['m_ts1'], name='ts1', text=[f"{val:.2%}" for val in yearly_data['m_ts1']],  texttemplate='%{text}',)) #, x= yearly_data.index, y= 'm_ts1', labels={'x':'Year', 'y':'% of Missing Data'}))
fig.add_trace(go.Bar(x = yearly_data.index, y =yearly_data['m_ts2'], name='ts2', text=[f"{val:.2%}" for val in yearly_data['m_ts2']],  texttemplate='%{text}',)) 

# Set the layout of the figure
fig.update_layout(
    title='Histograms for % of missing data of ts1 and ts2 by YEAR',
    xaxis_title='Year',
    yaxis_title='% Missing Data'
)
# Show the plot
fig.show()

fig2 = go.Figure()
fig2.add_trace(go.Bar(x = hourly_data.index, y =hourly_data['m_ts1'], name='ts1', text=[f"{val:.2%}" for val in hourly_data['m_ts1']],  texttemplate='%{text}',)) #, x= yearly_data.index, y= 'm_ts1', labels={'x':'Year', 'y':'% of Missing Data'}))
fig2.add_trace(go.Bar(x = hourly_data.index, y =hourly_data['m_ts2'], name='ts2', text=[f"{val:.2%}" for val in hourly_data['m_ts2']],  texttemplate='%{text}',)) 

# Set the layout of the figure
fig2.update_layout(
    title='Histograms for % of missing data of ts1 and ts2 by Hour of the Day',
    xaxis=dict(
        title = 'Hour of the Day',
        automargin=False,
        tickangle=45,
        dtick = 1
        ),
    yaxis_title='% Missing Data'
)
# Show the plot
fig2.show()
# print(yearly_data, hourly_data)


# Optimization module 
# para optimization for 2 parameters
# import trading model for function calling
from TF_Simple import TF_simple
# class for output return performance 
from Equity import Equity
import pandas as pd
import time
import plotly.express as px

# param1 = range for entry look back
# param2 = range for exit look back
#param1_range = range(200, 3800, 200)
#param2_range = range(50, 800, 50)
param1_range = range(2200, 2600, 500)
param2_range = range(450, 800, 400)

# generate cols for optimizaition result output 
cols = ['param1','param2','sharp','sortino','return','maxdd','num_trd']
df = pd.DataFrame(columns= cols)
rows = []
# Loop through the first parameter range
for param1 in param1_range:
    # Loop through the second parameter range
    for param2 in param2_range:
        # call signal module, last parameter is the cost use in the model
        signals = TF_simple(param1, param2, 0.00025)
        # call equity attribute for performance statistic . eg: avg return, maxdd, sharpe ratio ....
        eq = Equity(signals['return'])
        # Append a row with the parameter values and the corresponding performance numbers to data frame
        row = {'param1':param1, 'param2':param2, 'sharp':eq.get_sharpe(), 'sortino':eq.get_sortino(), 'return': eq.get_return(), 'maxdd':eq.get_maxdd(), 'num_trd':signals.iloc[-1]['num_trd']}
        print(row)
        rows.append(row)

df = pd.concat([df, pd.DataFrame(rows)])  
# output all optimizaition result to file 
df.to_csv('optsimple_1.csv')  
# output 3D optimization chart
fig = px.scatter_3d(df, x='param1', y='param2', z='sortino',  color = 'param2')
fig.show()

#end_time = time.time()
#print(f"Time taken for method 1: {end_time - start_time}")    

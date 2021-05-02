# python3

import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df_ini = pd.read_csv(
    '/home/taimur/Documents/DarkCirrus Projects/Analyzing Bit Records/data/Mid-Con ToolRun.csv')
df_ini = df_ini[df_ini['Bit Size']>10]
df_on_btm = df_ini[df_ini['Depth Out'] < 7000]
df_bits = df_on_btm['Bit Serial Number'].groupby(df_on_btm['Bit Mfg'])
df_bits = df_bits.describe()

'''fig = make_subplots(rows = 2, cols = 2,
                    specs=[[{"type": "xy"}, {"type": "domain"}],
                           [{"type": "xy"}, {"type": "domain"}]],
                    )

fig.add_trace(go.Scatter(x = df_on_btm['Distance'], y = df_on_btm['ROP']),
              row=1, col=1)

fig.add_trace(go.Scatter(x = df_on_btm['Distance'], y = df_on_btm['Hrs']),
              row=2, col=1)

fig.add_trace(go.Pie(labels = df_bits.index.values,
                     values = df_bits['count']),
              row=1, col=2)

fig.add_trace(go.Pie(labels = df_bits.index.values,
                     values = df_bits['count']),
              row=2, col=2)

fig.show()
'''

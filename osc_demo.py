import numpy as np
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def horizontal_points(point_per_div=25, total_div=10):
  total_point = total_div * point_per_div
  return np.arange(-total_point, total_point+1)

st.title('Oscilloscope')
fq = 10000
amp = 2

time_per_div = 1e-5
point_per_div=25
total_div=10

total_point = total_div * point_per_div
time_per_point = time_per_div / point_per_div

vol_per_div_ch1 = 0.2

omega = 2*np.pi*fq

x = horizontal_points()
# x = np.arange(total_point+1)
y1 = amp * np.sin(omega*x*time_per_point)
y2 = -amp * np.sin(omega*x*time_per_point)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y1,
                    mode='lines',
                    name='CH1',
                    xaxis='x',
                    yaxis='y',
                    hoverinfo='skip'))

fig.add_trace(go.Scatter(x=x, y=y2,
                    mode='lines',
                    name='CH2',
                    xaxis='x',
                    yaxis='y2',
                    hoverinfo='skip'))

lower_bound = -total_point//2
upper_bound = total_point//2
# fig.update_xaxes(range=[lower_bound, upper_bound])
# fig.update_xaxes(tick0=lower_bound, dtick=point_per_div)
fig.update_layout(xaxis=dict(range=[lower_bound, upper_bound], 
                             tick0=lower_bound,
                             dtick=point_per_div, 
                             showticklabels=False,
                             ))
lower_bound = -1*4
upper_bound = 1*4
fig.update_layout(yaxis=dict(range=[lower_bound, upper_bound], 
                             showticklabels=False,
                             zeroline=True,
                             zerolinewidth=4, 
                             ))

lower_bound = -1*2
upper_bound = 1*2
fig.update_layout(yaxis2=dict(range=[lower_bound, upper_bound], 
                              showticklabels=False, 
                              overlaying='y', 
                              ))

st.plotly_chart(fig, use_container_width=True)

import numpy as np
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def horizontal_points(point_per_div=25, total_div=10):
  total_point = total_div * point_per_div
  return np.arange(-total_point, total_point+1)

st.title('Oscilloscope')

# Sidebar for funcction generator to be set 
st.sidebar.title('Function Generator')
fq = st.sidebar.number_input('Frequency [Hz]', value=10000)
amp = st.sidebar.number_input('Amp Voltage [V]', value=2)

# OSC Display
main_dsp = st.container()
main_dsp.header('Display')

# ADJ Panel
col1, col2, col3 = st.columns(3)

dict_vol ={'5V': 5, '2V': 2, '1V': 1, '500mV': .5, '200mV': .2, '100mV': .1, '50mV': .05, '20mV': .02}

dict_time = {'25ms': 2.5e-2, '10ms': 1e-2, '5ms': 5e-3, 
             '2.5ms': 2.5e-3, '1ms': 1e-3, '500μs': 5e-4, 
             '250μs': 2.5e-4, '100μs': 1e-4, '50μs': 5e-5, 
             '25μs': 2.5e-5, '10μs': 1e-5, '5μs': 5e-6
            }
                          
with col1:
#   st.header('CH1')
  vol_ind = st.selectbox('VOLTS/DIV (CH1)', dict_vol, 2)
  vol_per_div_ch1 = dict_vol.get(vol_ind)
  st.write(vol_per_div_ch1)

with col2:
#   st.header('CH2')
  vol_ind = st.selectbox('VOLTS/DIV (CH2)', dict_vol, 2)
  vol_per_div_ch2 = dict_vol.get(vol_ind)
  st.write(vol_per_div_ch2)
  
with col3:
#   st.header('TIME')
  time_ind = st.selectbox('TIME/DIV', dict_time, 10)
  time_per_div = dict_time.get(time_ind)
  st.write(time_per_div)

# OSC Settings
point_per_div = 25
total_div = 10

time_per_point = time_per_div / point_per_div
total_point = total_div * point_per_div

total_div_v = 8

# Create Waveforms
vol_per_div_ch1 = 0.2

x = horizontal_points()
omega = 2*np.pi*fq

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
fig.update_layout(xaxis=dict(range=[lower_bound, upper_bound], 
                             tick0=lower_bound,
                             dtick=point_per_div, 
                             showticklabels=False,
                             ))

fig.update_layout(yaxis=dict( 
                             showticklabels=False,
                             zeroline=True,
                             zerolinewidth=2, 
                             ))

fig.update_layout(yaxis2=dict( 
                              showticklabels=False, 
                              zeroline=False,
                              overlaying='y', 
                              ))

lower_bound1 = -vol_per_div_ch1*total_div_v//2
upper_bound1 = vol_per_div_ch1*total_div_v//2

lower_bound2 = -vol_per_div_ch2*total_div_v//2
upper_bound2 = vol_per_div_ch2*total_div_v//2

fig.update_layout(yaxis=dict(range=[lower_bound1, upper_bound1], 
                             tick0=lower_bound,
                             dtick=vol_per_div_ch1, 
                             ),
                  yaxis2=dict(range=[lower_bound2, upper_bound2], 
                              # overlaying='y', 
                              ))

main_dsp.plotly_chart(fig)
# main_dsp.plotly_chart(fig, use_container_width=True)


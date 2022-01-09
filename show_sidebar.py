import streamlit as st
import numpy as np
import pandas as pd
import base64 
import altair as alt
# from scipy import signal

st.title('Oscilloscope')

# Sidebar for funcction generator to be set 
st.sidebar.title('Function Generator')
fq = st.sidebar.number_input('Frequency [Hz]', value=10000)
amp = st.sidebar.number_input('Amp Voltage [V]', value=2)

# OSC Display
main_dsp = st.container()
main_dsp.header('Display')

# OSC settings
h_pos = st.slider('Horizontal position', min_value=-1.0, max_value=1.0, )

point_per_div = 25
total_div = 10

col1, col2, col3 = st.columns(3)

df_vol = pd.DataFrame({
  'ind': ['5V', '2V', '1V', '500mV', '200mV', '100mV', '50mV', '20mV'],
  'val': [5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02],
})

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
  st.write(time_per_div1)

# time_per_div = 1.0e-5
time_per_point = time_per_div / point_per_div
total_point = total_div * point_per_div


# Create Waveforms
x = np.arange(total_point+1)

# omega = 2*np.pi*fq/time_per_div/100
omega = 2*np.pi*fq
# omega = 0.2

source = pd.DataFrame({
  'x': x,
  'f(x)': amp * np.sin(omega*x*time_per_point)
})

c = alt.Chart(source,width=600,height=400).mark_line().encode(
  x = 'x',
#   alt.X('x', scale=alt.Scale(domain=(0, 100)),title="Time"),
  y = 'f(x)',
)

main_dsp.altair_chart(c)


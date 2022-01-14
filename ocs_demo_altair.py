import datetime
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

def pnt_now(text=''):
  DIFF_JST_FROM_UTC = 9
  dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
  st.write(text,dt_now.strftime('%Y-%m-%d %H:%M:%S'))

def strtime_now_jst():
  DIFF_JST_FROM_UTC = 9
  dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
  return dt_now.strftime('%Y-%m-%d %H:%M:%S')

@st.cache
def h_point_array(h_total_point):
  return np.arange(-h_total_point, h_total_point+1)

@st.cache
def sin_waveform_array(fq, h_point_array, time_per_div=1e-5, h_point_per_div=25):
#   pnt_now('wave_form')
  time_per_point = time_per_div / h_point_per_div
  x = h_point_array
  omega = 2*np.pi*fq
  return np.sin(omega*x*time_per_point)

@st.cache
def div_vals():
  dict_vol ={'5V': 5, '2V': 2, '1V': 1, '500mV': .5, '200mV': .2, '100mV': .1, '50mV': .05, '20mV': .02}

  dict_time = {'25ms': 2.5e-2, '10ms': 1e-2, '5ms': 5e-3, 
               '2.5ms': 2.5e-3, '1ms': 1e-3, '500μs': 5e-4, 
               '250μs': 2.5e-4, '100μs': 1e-4, '50μs': 5e-5, 
               '25μs': 2.5e-5, '10μs': 1e-5, '5μs': 5e-6
              }
  return dict_vol, dict_time

# Config horizontal params and estimate x-axis points
h_point_per_div = 25
h_total_div = 10
h_total_point = h_total_div * h_point_per_div
x = h_point_array(h_total_point)

# Config vertical params
v_point_per_div = 25
v_total_div = 8
v_total_point = v_point_per_div * v_total_div

# Display title
st.title('Oscilloscope')

# Sidebar for funcction generator to be set 
st.sidebar.title('Function Generator')
fq = st.sidebar.number_input('Frequency [Hz]', value=10000)
amp = st.sidebar.number_input('Amp Voltage [V]', value=2)
beta = 0.7

# OSC Display
main_dsp = st.container()
main_dsp.header('Display')

# ADJ Panel
col1, col2, col3 = st.columns(3)

dict_vol, dict_time = div_vals()

with col1:
#   st.header('CH1')
  vol_ind_ch1 = st.selectbox('VOLTS/DIV (CH1)', dict_vol, 2)
  vol_per_div_ch1 = dict_vol.get(vol_ind_ch1)
  st.write(vol_per_div_ch1)

with col2:
#   st.header('CH2')
  vol_ind_ch2 = st.selectbox('VOLTS/DIV (CH2)', dict_vol, 2)
  vol_per_div_ch2 = dict_vol.get(vol_ind_ch2)
  st.write(vol_per_div_ch2)
  
with col3:
#   st.header('TIME')
  time_ind = st.selectbox('TIME/DIV', dict_time, 10)
  time_per_div = dict_time.get(time_ind)
  waveform = sin_waveform_array(fq, x, time_per_div, h_point_per_div)
  st.write(time_per_div)

# OSC Settings
vol_per_point_ch1 = vol_per_div_ch1 / v_point_per_div
vol_per_point_ch2 = vol_per_div_ch2 / v_point_per_div

y1 = amp / vol_per_point_ch1 * waveform
y2 = beta * amp / vol_per_point_ch2 * waveform

# Show fig
source = pd.DataFrame({'x':x, 'y1':y1, 'y2':y2})

xlim = (-h_total_point//2, h_total_point//2)
ylim = (-v_total_point//2, v_total_point//2)

ylim2 = (-v_total_point, v_total_point)

base = alt.Chart(source).encode(
    x=alt.X('x:Q', axis=alt.Axis(title=None), scale=alt.Scale(domain=xlim)) 
).properties(width=400, height=400)
  
line1 = base.mark_line(clip=True).encode(
    y=alt.Y('y1:Q', scale=alt.Scale(domain=ylim)),
)    
    
line2 = base.mark_line(clip=True).encode(
    y=alt.Y('y2:Q', scale=alt.Scale(domain=ylim2))
)    

c = alt.layer(line1, line2).resolve_scale(
    y = 'independent'
)

st.altair_chart(c, use_container_width=False)

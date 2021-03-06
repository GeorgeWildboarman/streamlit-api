from io import BytesIO
import datetime
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

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

@st.cache
def creat_fig(h_total_point, v_total_point):
  fig, ax = plt.subplots(1, 1, figsize=[10, 10])

  ax.set(aspect=1, xlim=(-h_total_point//2, h_total_point//2), ylim=(-v_total_point//2, v_total_point//2))

  ax.set_xticks(np.linspace(-h_total_point//2, h_total_point//2, h_total_div+1, endpoint=True), minor=False, )
  ax.set_yticks(np.linspace(-v_total_point//2, v_total_point//2, v_total_div+1, endpoint=True), minor=False, )

  ax.spines['bottom'].set_position('zero')
  ax.spines['left'].set_position('zero')

  ax.set_xticklabels([])
  ax.set_yticklabels([])

  ax.minorticks_on()

  ax.grid(which="major", color="black", alpha=1)
  ax.grid(which="minor", color="gray", linestyle='--')
  
  return fig, ax

  
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

pnt_now()

# Show fig
fig, ax = creat_fig(h_total_point, v_total_point)

param_dict = dict(color='red', linewidth=1, label='CH1')
ax.plot(x, y1, **param_dict)

param_dict = dict(color='blue', linewidth=1, label='CH2')
ax.plot(x, y2, **param_dict)

text = '{:,}Hz'.format(fq)
fig.text(.9, .2, text, verticalalignment='bottom', horizontalalignment='right')

text = 'CH1 VOLTS/DIV={:<10}TIME/DIV={:<6}\nCH2 VOLTS/DIV={:<10}'.format(vol_ind_ch1, time_ind, vol_ind_ch2)
fig.text(.1, .2, text, horizontalalignment='left', bbox={'boxstyle':'round', 'facecolor':'white'})

text = strtime_now_jst()
fig.text(.15, .8, text, horizontalalignment='left')

main_dsp.pyplot(fig)

# def convert_plt(fig):
#   pnt_now('convert_plt')
#   ofs = BytesIO()
#   fig.savefig(ofs, format='png')
#   return ofs

# png = convert_plt(fig)
# file_name = '{:06_}Hz.png'.format(fq)

# st.download_button(
#   label="Download Fig as PNG", 
#   data=png,
#   file_name=file_name,
#   mime='image/png',
#  )




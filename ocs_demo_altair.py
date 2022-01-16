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
  # horizontal points in OSC display coordinate
  return np.arange(-h_total_point, h_total_point+1)

def cal_gain_and_phase(fq, C=0.01e-6, R=6.8e3):
  omega = 2*np.pi*fq
  be = (omega*C*R)**3/(((omega*C*R)**3-5*omega*C*R)-1j*(6*(omega*C*R)**2-1))
  return np.abs(be), np.arctan2(be.imag, be.real)

@st.cache
def sin_func_gen(fq, h_total_point, time_per_point, gain, theta):
  '''
  Create pandas DF with 3 columns: x, v1, v2
  x  : horizontal point in OCS display coordinate 
  v1 : sine wave function
  v2 : sine wave function transformed by CRx3 filter 
  '''
  # horizontal points in OSC display coordinate
  x = h_point_array(h_total_point)
  
  omega = 2*np.pi*fq
  # Generate sine wave
  y1 = np.sin(omega*x*time_per_point)
  
  # Transformed wave
  y2 = gain*np.sin(omega*x*time_per_point+theta)

  # Create pandas DF and return it
  return pd.DataFrame({'x':x, 'y1':y1, 'y2':y2, 'label1':['CH1']*len(x), 'label2':['CH2']*len(x)})
  
def div_vals():
  dict_vol ={'5V': 5, '2V': 2, '1V': 1, '500mV': .5, '200mV': .2, '100mV': .1, '50mV': .05, '20mV': .02}

  dict_time = {'25ms': 2.5e-2, '10ms': 1e-2, '5ms': 5e-3, 
               '2.5ms': 2.5e-3, '1ms': 1e-3, '500μs': 5e-4, 
               '250μs': 2.5e-4, '100μs': 1e-4, '50μs': 5e-5, 
               '25μs': 2.5e-5, '10μs': 1e-5, '5μs': 5e-6
              }
  return dict_vol, dict_time

# Config horizontal axis for OCS
h_point_per_div = 50
h_total_div = 10
h_total_point = h_total_div * h_point_per_div

# Config vertical axis for OCS
v_point_per_div = 50
v_total_div = 8
v_total_point = v_point_per_div * v_total_div

# Create sidebar for FG front panel 
st.sidebar.title('Function Generator')
# Select params on FG
fq = st.sidebar.number_input('Frequency [Hz]', value=10000)
amp = st.sidebar.number_input('Amp Voltage [V]', value=2)

# Display title
st.title('Oscilloscope')

# Create OSC Display
main_dsp = st.container()
main_dsp.header('Display')

# Create OSC ADJ Panel
col1, col2, col3 = st.columns(3)

# Select OCS params
dict_vol, dict_time = div_vals()
with col1:
#   st.header('CH1')
  vol_ind_ch1 = st.selectbox('VOLTS/DIV (CH1)', dict_vol, 2)
  vol_per_div_ch1 = dict_vol.get(vol_ind_ch1)
  vol_per_point_ch1 = vol_per_div_ch1 / v_point_per_div
  st.write(vol_per_div_ch1)

with col2:
#   st.header('CH2')
  vol_ind_ch2 = st.selectbox('VOLTS/DIV (CH2)', dict_vol, 2)
  vol_per_div_ch2 = dict_vol.get(vol_ind_ch2)
  vol_per_point_ch2 = vol_per_div_ch2 / v_point_per_div
  st.write(vol_per_div_ch2)
  
with col3:
#   st.header('TIME')
  time_ind = st.selectbox('TIME/DIV', dict_time, 10)
  time_per_div = dict_time.get(time_ind)
  time_per_point = time_per_div / h_point_per_div
  st.write(time_per_div)

# Generate wave function
gain, theta = cal_gain_and_phase(fq, 0.01e-6, 6.8e3)
pf_wave = sin_func_gen(fq, h_total_point, time_per_point, gain, theta)
# x, y1, y2 = sin_func_gen(fq, h_total_point, time_per_point, 0.01e-6, 6.8e3)
# x, y1, y2 = sin_func_gen(fq, h_total_point, time_per_point, gain, theta)
# pf_wave = pd.DataFrame({'x':x, 'y1':y1, 'y2':y2})

# -------------------------------------
# Show fig as OSC Display
# -------------------------------------

# vertical and horizontal ranges
xlim = (-h_total_point//2, h_total_point//2)
ylim = (-v_total_point//2, v_total_point//2)

# Legend Setting
domain = ['CH1', 'CH2']
range_ = ['orange', 'deepskyblue']
# 'deepskyblue'
# 'dodgerblue'
# 'royalblue'

# Draw grid lines
sub_grid_ticks = 5
h_grid_val = np.linspace(*xlim, h_total_div+1, endpoint=True)
pf_xgrid = pd.DataFrame({'val':h_grid_val})
total_sub_xgrid = h_total_div*sub_grid_ticks+1

v_grid_val = np.linspace(*ylim, v_total_div+1, endpoint=True)
pf_ygrid = pd.DataFrame({'val':v_grid_val})
total_sub_ygrid = v_total_div*sub_grid_ticks+1


ygrid_lines = alt.Chart(pf_ygrid).mark_rule(color='white').encode(
    y=alt.Y('val:Q',
            scale=alt.Scale(domain=ylim),
            axis=alt.Axis(title=None,
                          grid=True,
                          gridColor='gray',
                          gridDash=[2],
                          labels=False,
                          ticks=False,
                          # tickMinStep=sub_grid_ticks,
                          tickCount=total_sub_ygrid
            )
    )
)

xgrid_lines = alt.Chart(pf_xgrid).mark_rule(color='white').encode(
    x=alt.X('val:Q',
            scale=alt.Scale(domain=xlim),
            axis=alt.Axis(title=None,
                          grid=True,
                          gridColor='gray',
                          gridDash=[2],
                          labels=False,
                          ticks=False,
                          tickCount=total_sub_xgrid,
            )
    )
)    

# Draw waveforms
offset = 0
base = alt.Chart(pf_wave).encode(
    x=alt.X('x:Q', axis=alt.Axis(title=None, grid=True), scale=alt.Scale(domain=xlim)) 
).transform_calculate(
    x=alt.datum.x
).properties(width=550, height=550)

# slider = alt.binding_range(min=-h_total_point//2, max=h_total_point//2, step=1, name='horizontal position')
# selector = alt.selection_single(name='SelectorName', fields=['offset'], bind=slider, init={'offset':20})

# base = alt.Chart(pf_wave).encode(
#     x=alt.X('x:Q', axis=alt.Axis(title=None, grid=True), scale=alt.Scale(domain=xlim)) 
# ).add_selection(selector).transform_calculate(
#     x=alt.datum.x + selector.offset
# ).properties(width=550, height=400)

line1 = base.mark_line(clip=True, color='orange').encode(
    y=alt.Y('y:Q', scale=alt.Scale(domain=ylim), title='CH1'),
    color=alt.Color(
        'label1', 
        legend=alt.Legend(title="", orient='none', legendX=500, legendY=5, fillColor='black', labelColor='white'), 
        scale=alt.Scale(domain=domain, range=range_)
    )
).transform_calculate(
    y=alt.datum.y1*amp/vol_per_point_ch1
)

line2 = base.mark_line(clip=True, color='blue').encode(
    y=alt.Y('y:Q', scale=alt.Scale(domain=ylim), title='CH2'),
    color=alt.Color(
        'label2', 
        legend=alt.Legend(title="", orient='none', legendX=500, legendY=20, fillColor='black', labelColor='white'),
        scale=alt.Scale(domain=domain, range=range_)
    )
).transform_calculate(
    y=alt.datum.y2*amp/vol_per_point_ch2
)    

# c = xgrid_lines + ygrid_lines +line1 + line2

c = alt.layer(xgrid_lines, ygrid_lines, line1, line2).configure(background='black')

main_dsp.altair_chart(c, use_container_width=False)

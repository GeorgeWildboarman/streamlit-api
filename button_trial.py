import datetime
import numpy as np
import pandas as pd
import streamlit as st

def pnt_now(text='Timestanp'):
  DIFF_JST_FROM_UTC = 9
  dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
  st.write(text,dt_now.strftime('%Y-%m-%d %H:%M:%S'))

def strtime_now_jst():
  DIFF_JST_FROM_UTC = 9
  dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
  return dt_now.strftime('%Y-%m-%d %H:%M:%S')

def h_point_array(h_total_point):
  # horizontal points centering on zero
  return np.arange(-h_total_point//2, h_total_point//2)

# @st.cache(allow_output_mutation=True)
@st.cache(suppress_st_warning=True)
def read_waveform_file(filename='A0000CH1.CSV'):
  # Read waveform file into Pandas DataFrame
  # Waveform file format : csv
  pnt_now('Run[read_waveform_file]')
  
  df=pd.read_csv(filename, header=None)

  # Put the data into settup information and waveform
  # The wave file includes settup information other than waveform data.
  # Settup info:
  df_info=df.iloc[:16,].set_index(0)
  # Waveform data:
  df_waveform = pd.DataFrame()
  df_waveform['raw']=pd.Series(df.iloc[16:,0], dtype='int')
  df_waveform.reset_index(drop=True, inplace=True)

  # Waveform data format
  # Vertical:
  # 1division includes 25 points of vertical data.
  # The vertical point starts from the GND level. 
  v_points_per_div = 25
  # 256 points in total (8bit)
  v_total_points = 256
  # Vertical Units	: V
  v_units = str(df_info.loc['Vertical Scale'])
  # Vertical Scale
  vol_per_div =float(df_info.loc['Vertical Scale'])
  vol_per_point = vol_per_div / v_points_per_div
  # Vertical offset [V]
  v_offset =float(df_info.loc['Vertical Position'])

  # Horizontal:
  # 1division includes 250 points of horizontal data.
  h_points_per_div = 250
  # 16div in horizontal axis with each 8div from screen center
  h_div = 16
  # 4000 points in total
  h_total_points = h_div * h_points_per_div 
  # Horizontal Units	: s
  h_units = str(df_info.loc['Horizontal Scale'])
  # Horizontal Scale
  time_per_div =float(df_info.loc['Horizontal Scale'])
  time_per_point = time_per_div/h_points_per_div
  # Horizontal offset [s]
  h_offset =float(df_info.loc['Horizontal Position'])

  # Add practical data
  df_waveform['time[s]'] = h_point_array(h_total_points)*time_per_point
  df_waveform['volts[V]'] = df_waveform['raw']*vol_per_point

  return df_waveform

def mmt_waveform(time_per_point=1.0e-6):
  '''
  Create pandas DF with 5 columns: t, v1, v2, label1, label2
  t  : horizontal point in OCS display coordinate 
  v1 : observed waveform
  v2 : filled with Not a Number 
  label1 : Norminal column for fig legend in Altair
  label2 : Norminal column for fig legend in Altair
  '''
  # read waveform file obtained from OSC:DCS-4605 
  df_waveform = read_waveform_file(filename='A0000CH1.CSV')
  # Arrange for display  
  df = pd.DataFrame({
      't':df_waveform['time[s]']/time_per_point, 
      'v1':df_waveform['volts[V]'], 
      'v2':[np.nan]*len(df_waveform), 
      'label1':['CH1']*len(df_waveform), 
      'label2':['CH2']*len(df_waveform), 
      })
  return df

# Statement of Changes in cache
stmt = st.container()
  
# Create sidbar to draw FG fromt panel
fg_panel = st.sidebar
fg_panel.title('Function Generator')

# Add input to set freq and amp
fq_inp = fg_panel.number_input('Frequency [Hz]', value=10000, step=10)
amp_inp = fg_panel.number_input('Amp Voltage [V]', value=2, step=1)

# Add radio to select task
def task_desc_for_radio(task):
  if 'gen' in task:
    return 'Wave from funcgen'
  elif 'file' in task:
    return 'wavefrom file'

task = fg_panel.radio("Select task", ('funcgen', 'wavefile'), 1, format_func=task_desc_for_radio, key='type')
fg_panel.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
fg_panel.write(task)

if 'gen' in task:
  fq = fq_inp
  amp = amp_inp
  st.write('task : funcgen')
elif 'file' in task:
  fq = np.nan
  amp =1
  pf_wave = mmt_waveform()
  st.write('task : file')
  st.write(pf_wave)

st.write('freq:', fq)

st.write('Amp:', amp)

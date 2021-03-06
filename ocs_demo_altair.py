import datetime
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import altair as alt

def pnt_now(text='Timestamp'):
  DIFF_JST_FROM_UTC = 9
  dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
  st.write(text,dt_now.strftime('%Y-%m-%d %H:%M:%S'))

def strtime_now_jst():
  DIFF_JST_FROM_UTC = 9
  dt_now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
  return dt_now.strftime('%Y-%m-%d %H:%M:%S')

@st.cache
def h_point_array(h_total_point):
  # horizontal points centering on zero
  return np.arange(-h_total_point//2, h_total_point//2)

def cal_gain_and_phase(fq, C=0.01e-6, R=6.8e3):
  omega = 2*np.pi*fq
  be = (omega*C*R)**3/(((omega*C*R)**3-5*omega*C*R)-1j*(6*(omega*C*R)**2-1))
  return np.abs(be), np.arctan2(be.imag, be.real)


@st.cache(suppress_st_warning=True)
def sin_func_gen(fq, h_total_point, time_per_point, gain, theta):
  '''
  Create pandas DF with 5 columns: t, v1, v2, label1, label2
  t  : horizontal point in OCS display coordinate 
  v1 : sine wave function
  v2 : sine wave function transformed by CRx3 filter 
  label1 : Norminal column for fig legend in Altair
  label2 : Norminal column for fig legend in Altair
  '''
#   pnt_now('Run[sin_func_gen]')
  # horizontal points in OSC display coordinate
  t = h_point_array(h_total_point*2)
  
  omega = 2*np.pi*fq
  # Generate sine wave
  v1 = np.sin(omega*t*time_per_point)
  
  # Transformed wave
  v2 = gain*np.sin(omega*t*time_per_point+theta)

  # Create pandas DF and return it
  return pd.DataFrame({'t':t, 'v1':v1, 'v2':v2, 'label1':['CH1']*len(t), 'label2':['CH2']*len(t)})

@st.cache
def read_waveform_file(filename='A0000CH1.CSV'):
  # Read waveform file into Pandas DataFrame
  # Waveform file format : csv
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

@st.cache(suppress_st_warning=True)
def mmt_waveform(time_per_point=1.0e-6):
  '''
  Create pandas DF with 5 columns: t, v1, v2, label1, label2
  t  : horizontal point in OCS display coordinate 
  v1 : observed waveform
  v2 : filled with Not a Number 
  label1 : Norminal column for fig legend in Altair
  label2 : Norminal column for fig legend in Altair
  '''
#   pnt_now('Run[mmt_waveform]')
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

def div_vals():
  dict_vol ={'5V': 5, '2V': 2, '1V': 1, '500mV': .5, '200mV': .2, '100mV': .1, '50mV': .05, '20mV': .02}

  dict_time = {'25ms': 2.5e-2, '10ms': 1e-2, '5ms': 5e-3, 
               '2.5ms': 2.5e-3, '1ms': 1e-3, '500??s': 5e-4, 
               '250??s': 2.5e-4, '100??s': 1e-4, '50??s': 5e-5, 
               '25??s': 2.5e-5, '10??s': 1e-5, '5??s': 5e-6
              }
  return dict_vol, dict_time

st.set_page_config(initial_sidebar_state='expanded')

# Config horizontal axis for OCS
h_point_per_div = 50
h_total_div = 10
h_total_point = h_total_div * h_point_per_div

# Config vertical axis for OCS
v_point_per_div = 50
v_total_div = 8
v_total_point = v_point_per_div * v_total_div

# Fig size
fig_height = 600
fig_width = 640

# Create sidebar to draw FG fromt panel
fg_panel = st.sidebar
fg_panel.title('Function Generator')

# Add input to set freq and amp
fq_inp = fg_panel.number_input('Frequency [Hz]', min_value=100, max_value=100000, value=10000, step=100, format='%d')
amp_inp = fg_panel.number_input('Amp Voltage [V]', value=2.0, step=1.0, format='%.3f')

# Add radio to select wave
def format_selected_wave(wave):
  if 'sine' in wave:
    return format(' Sine waveform ', '*^26')
  elif 'osc' in wave:
    return format(' Oscillation waveform ', '*^26')

selected_wave = fg_panel.radio("Select waveform", ('sine', 'oscillation'), 0, format_func=format_selected_wave)
# fg_panel.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# Create OSC Display
main_dsp = st.container()
main_dsp.title('Oscilloscope')
# main_dsp.header('Display')

# vertical and horizontal ranges
xlim = (-h_total_point//2, h_total_point//2)
ylim = (-v_total_point//2, v_total_point//2)

# Slider for horizontal position
# h_offset_div = st.number_input('Horizontal Position [DIV]', -h_total_div*.5, h_total_div*.5, 0.0, 1./h_point_per_div, '%.2f') 
h_offset_div = st.slider('Horizontal Position [DIV]', -h_total_div*.5, h_total_div*.5, 0.0, 1./h_point_per_div, '%.2f') 
h_offset = h_offset_div*h_point_per_div
# h_offset = st.slider('Horizontal Position', *xlim, 0, 1, '') 

# Create OSC ADJ Panel
col1, col2, col3 = st.columns(3)

# Select OCS params
dict_vol, dict_time = div_vals()
with col1:
#   st.header('CH1')
  vol_ind_ch1 = st.selectbox('VOLTS/DIV (CH1)', dict_vol, 2)
  vol_per_div_ch1 = dict_vol.get(vol_ind_ch1)
  vol_per_point_ch1 = vol_per_div_ch1 / v_point_per_div
#   st.write(vol_per_div_ch1)

with col2:
#   st.header('CH2')
  vol_ind_ch2 = st.selectbox('VOLTS/DIV (CH2)', dict_vol, 2)
  vol_per_div_ch2 = dict_vol.get(vol_ind_ch2)
  vol_per_point_ch2 = vol_per_div_ch2 / v_point_per_div
#   st.write(vol_per_div_ch2)
  
with col3:
#   st.header('TIME')
  time_ind = st.selectbox('TIME/DIV', dict_time, 10)
  time_per_div = dict_time.get(time_ind)
  time_per_point = time_per_div / h_point_per_div
#   st.write(time_per_div)

# Description of the experiments
desc_exp = st.container()
desc_exp.header('''

Descritption:
''')

if 'sine' in selected_wave:
  desc_exp.subheader('CR???????????????????????????????????????')
  img1 = Image.open('img/Img_3-1.jpg')
  img2 = Image.open('img/Fig_3-1.png')
  desc_exp.image(img1, width=fig_width)
  desc_exp.image(img2, width=fig_width)
  desc_exp.markdown('''
  * FG?????????????????????CR??????????????????????????????????????????????????????????????????????????????CH1???????????????????????????????????????????????????CH2??????????????????<br>
  * CH1???CH2????????????????????????????????????????????????????????????????????????????????????????????????????????????<br>
  * FG???????????????????????????????????????????????????????????????<br>
    - ??????: ?????????<br>
    - ??????: 2V<br>
    - ?????????: __ 10kHz???8kHz???6kHz???5kHz???4kHz???3kHz???2kHz???1kHz, 800Hz???600Hz???500Hz __ <br>
  ''', unsafe_allow_html=True)
elif 'osc' in selected_wave:
  desc_exp.subheader('CR????????????????????????????????????????????????')
  img1 = Image.open('img/Img_3-2.jpg')
  img2 = Image.open('img/Fig_3-2.png')
  desc_exp.image(img1, width=fig_width)
  desc_exp.image(img2, width=fig_width)
  desc_exp.markdown('''
  * ?????????CR??????????????????????????????9V??????????????????????????????????????????????????????????????????????????????<br>
  * ??????????????????????????????????????????CR??????????????????????????????????????????????????????????????????<br>
  * ???????????????????????????????????????????????????????????????????????????????????????????????????<br>
  ''', unsafe_allow_html=True)

# Generate waveforms
if 'sine' in selected_wave:
  fq = fq_inp
  amp = amp_inp
  # Generate wave function
  gain, theta = cal_gain_and_phase(fq, 0.01e-6, 6.8e3)
  pf_wave = sin_func_gen(fq, h_total_point, time_per_point, gain, theta)
elif 'osc' in selected_wave:
  fq = np.nan
  amp =1
  pf_wave = mmt_waveform(time_per_point)

# -------------------------------------
# Show fig as OSC Display
# -------------------------------------
# Legend Setting
domain = ['CH1', 'CH2']
range_ = ['orange', 'deepskyblue']
# 'deepskyblue'
# 'dodgerblue'
# 'royalblue'

# Draw grid lines
sub_grid_ticks = 5
grid_line_width = 0.5

h_grid_val = np.linspace(*ylim, v_total_div+1, endpoint=True)
pf_hgrid = pd.DataFrame({'val':h_grid_val})
total_sub_hgrid = v_total_div*sub_grid_ticks+1

h_grid_lines = alt.Chart(pf_hgrid).mark_rule(color='white').encode(
    y=alt.Y('val:Q',
            axis=alt.Axis(title=None,
                          grid=True,
                          gridColor='gray',
                          gridDash=[2],
                          labels=False,
                          ticks=False,
                          tickCount=total_sub_hgrid,
            ), scale=alt.Scale(domain=ylim),
    ),
    size = alt.value(grid_line_width)
)

v_grid_val = np.linspace(*xlim, h_total_div+1, endpoint=True)
pf_vgrid = pd.DataFrame({'val':v_grid_val})
total_sub_vgrid = h_total_div*sub_grid_ticks+1

v_grid_lines = alt.Chart(pf_vgrid).mark_rule(color='white').encode(
    x=alt.X('val:Q',
            axis=alt.Axis(title=None,
                          grid=True,
                          gridColor='gray',
                          gridDash=[2],
                          labels=False,
                          ticks=False,
                          tickCount=total_sub_vgrid, 
            ), scale=alt.Scale(domain=xlim),
    ),
    size = alt.value(grid_line_width)
)    

# Draw zoro lines
h_offsett_ch1 = 0
h_offsett_ch2 = 0
zoro_line_width = 1
v_zoro_line = alt.Chart(pd.DataFrame({'val':[0]})).mark_rule(
    color = 'white', 
).encode(
    alt.X('val:Q',),
    size=alt.value(zoro_line_width)
)

h_zoro_line_ch1 = alt.Chart(pd.DataFrame({'val':[h_offsett_ch1]})).mark_rule(
    color = 'white', 
).encode(
    alt.Y('val:Q',),
    size=alt.value(zoro_line_width)
)

h_zoro_line_ch2 = alt.Chart(pd.DataFrame({'val':[h_offsett_ch2]})).mark_rule(
    color = 'white', 
).encode(
    alt.Y('val:Q',),
    size=alt.value(zoro_line_width)
)

# Draw waveforms
base = alt.Chart(pf_wave).encode(
    x=alt.X('x:Q', 
#           axis=alt.Axis(title=None, grid=False, labels=False, ticks=False), 
          scale=alt.Scale(domain=xlim), 
          title='TIME',
    ) 
).transform_calculate(
    x=alt.datum.t*1+h_offset
)

legendX = fig_width * 0.9
legendY = 10
line1 = base.mark_line(clip=True, color='orange').encode(
    y=alt.Y('y:Q', 
#             axis=alt.Axis(title=None, grid=False, labels=False, ticks=False), 
            scale=alt.Scale(domain=ylim), 
            title='CH1',
    ),color=alt.Color(
        'label1', 
        legend=alt.Legend(title="", orient='none', legendX=legendX, legendY=legendY, fillColor='black', labelColor='white'), 
        scale=alt.Scale(domain=domain, range=range_)
    ),
).transform_filter(
    'isValid(datum.v1)'
).transform_calculate(
    y=alt.datum.v1*amp/vol_per_point_ch1
)

line2 = base.mark_line(clip=True, color='blue').encode(
    y=alt.Y('y:Q', 
#             axis=alt.Axis(title=None, grid=False, labels=False, ticks=False), 
            scale=alt.Scale(domain=ylim), 
            title='CH2', 
    ),color=alt.Color(
        'label2', 
        legend=alt.Legend(title="", orient='none', legendX=legendX, legendY=legendY+20, fillColor='black', labelColor='white'),
        scale=alt.Scale(domain=domain, range=range_)
    )
).transform_filter(
    'isValid(datum.v2)'
).transform_calculate(
    y=alt.datum.v2*amp/vol_per_point_ch2
)    

# Write info on display
df_txt = pd.DataFrame(columns=['x', 'y', 'txt'])

info = 'CH1 VOLTS/DIV={:<8}'.format(vol_ind_ch1)
df_txt.loc['scale1']= [xlim[0], ylim[0]-v_point_per_div*.2, info]
info = 'CH2 VOLTS/DIV={:<8}'.format(vol_ind_ch2)
df_txt.loc['scale2']= [xlim[0], ylim[0]-v_point_per_div*.5, info]
info = strtime_now_jst()
df_txt.loc['time'] = [xlim[0], ylim[1]+v_point_per_div*.2, info]

text_l = alt.Chart(df_txt).mark_text(align='left', baseline='middle', color='red').encode(
    alt.X('x:Q'),
    alt.Y('y:Q'),
    text='txt:N'
)

df_txt_r = pd.DataFrame(columns=['x', 'y', 'txt'])
info = format_selected_wave(selected_wave)
df_txt_r.loc['wave'] = [xlim[1]+h_point_per_div*.2, ylim[1]+v_point_per_div*.2, info]
info = 'Frequency={:>7,} Hz'.format(fq)
df_txt_r.loc['fq'] = [xlim[1]-h_point_per_div*.2, ylim[0]-v_point_per_div*.2, info]
df_txt_r.loc['v_zero_point'] = [xlim[0], 0, '0>']

text_r = alt.Chart(df_txt_r).mark_text(align='right', baseline='middle', color='red').encode(
    alt.X('x:Q'),
    alt.Y('y:Q'),
    text='txt:N'
)

df_txt_c = pd.DataFrame(columns=['x', 'y', 'txt'])
# df_txt_c.loc['annotation']= [0, ylim[1]+v_point_per_div*.2, 'SAMPLE']
info = 'TIME/DIV={:<6}'.format(time_ind)
df_txt_c.loc['scaleT']= [0, ylim[0]-v_point_per_div*.2, info]
text_c = alt.Chart(df_txt_c).mark_text(align='center', baseline='middle', color='red').encode(
    alt.X('x:Q'),
    alt.Y('y:Q'),
    text='txt:N'
)

c = alt.layer(
  line1,
  line2,
  v_grid_lines,
  h_grid_lines,
  text_l,
  text_r,
  text_c,
  v_zoro_line,
  h_zoro_line_ch1,
).configure(background='black').properties(width=fig_width, height=fig_height)

main_dsp.altair_chart(c, use_container_width=False)


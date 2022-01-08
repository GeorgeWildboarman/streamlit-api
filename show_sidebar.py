import streamlit as st
import numpy as np
import pandas as pd
import base64 
import altair as alt
# from scipy import signal

st.title('Oscilloscope')

xp = np.linspace(0,100,100)
zp = np.zeros_like(xp)

x = np.arange(100)

st.sidebar.title('Function Generator')
x1=st.sidebar.text_input('Frequency [Hz]',10000)
x2=st.sidebar.text_input('Amp Voltage [V]',2)
# y1=st.sidebar.text_input('Input Y1 here',10)
# y2=st.sidebar.text_input('Input Y2 here',20)
# density=st.sidebar.text_input('Input Model Density contrast here (background - body)',2000)

time_per_div = 1.0e-4
fq = float(x1)
x2 = float(x2)
# omega = 2*np.pi*fq/time_per_div/100
omega = 2*np.pi/10

source = pd.DataFrame({
  'x': x,
  'f(x)': x2 * np.sin(omega*x)
})

c = alt.Chart(source,width=600,height=400).mark_line().encode(
  alt.X('x', scale=alt.Scale(domain=(0, 100)),title="Time"),
  y='f(x)',
)

st.altair_chart(c)
h_pos = st.slider('Horizontal position', min_value=-1.0, max_value=1.0, )

# x1=float(x1)
# x2=float(x2)
# y1=float(y1)
# y2=float(y2)
# density=float(density)
# line = gz(xp,zp,x1,x2,y1,y2,density)


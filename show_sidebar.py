import streamlit as st
import numpy as np
import pandas as pd
import base64 
import altair as alt

st.title('Oscilloscope')

xp = np.linspace(0,100,100)
zp = np.zeros_like(xp)

st.sidebar.title('Function Generator')
x1=st.sidebar.text_input('Input X1 here',30)
x2=st.sidebar.text_input('Input X2 here',40)
y1=st.sidebar.text_input('Input Y1 here',10)
y2=st.sidebar.text_input('Input Y2 here',20)
density=st.sidebar.text_input('Input Model Density contrast here (background - body)',2000)


x1=float(x1)
x2=float(x2)
y1=float(y1)
y2=float(y2)
density=float(density)
line = gz(xp,zp,x1,x2,y1,y2,density)


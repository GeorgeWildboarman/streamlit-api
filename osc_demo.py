import numpy as np
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.title('Oscilloscope')

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)

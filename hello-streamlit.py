import os
import socket
import streamlit as st

st.write('Hello Streamlit again!!!')
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

st.write(hostname,ip)

# st.write(dict(os.environ))

st.write('hello<br>hello<br>')

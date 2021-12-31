# import streamlit as st
# import numpy as np
# import pandas as pd

# your_name = st.text_input("Enter your name", max_chars=10)
# st.title(your_name)

# number = st.number_input("Enter number", 0, 25, 6, 2)

# my_date = st.date_input("Select date") 
# st.write(my_date)

# vol_1 = st.number_input('Enter vol[mV]')

# ----------------------------------------------------------------------------
# Randomly fill a dataframe and cache it
# @st.cache(allow_output_mutation=True)
# def get_dataframe():
#     return pd.DataFrame(
#         np.random.randn(50, 20),
#         columns=('col %d' % i for i in range(20)))


# df = get_dataframe()

# # Create row, column, and value inputs
# row = st.number_input('row', max_value=df.shape[0])
# col = st.number_input('column', max_value=df.shape[1])
# value = st.number_input('value')

# # Change the entry at (row, col) to the given value
# df.values[row][col] = value

# # And display the result!
# st.dataframe(df)

# -----------------------------------------------------------------------------
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

if 'init' not in st.session_state: st.session_state['init']=False
if 'store' not in st.session_state: st.session_state['store']={}
if 'store_d' not in st.session_state: st.session_state['store_d']={}
if 'edit' not in st.session_state: st.session_state['edit']=True

if st.session_state.init == False:
    st.session_state.store_d = {'A':[1,2,3,4], 'B':[7,6,5,4]}
    st.session_state.init = True

@st.cache(allow_output_mutation=True)
def fetch_data():
    return pd.DataFrame(st.session_state.store_d)

def saveDefault():
    st.session_state.store_d = st.session_state.store
    return

def app():
    c1,c2=st.columns(2)
    lock=c1.button('Lock', key='lock', on_click=saveDefault)
    unlock=c2.button('Unlock', key='unlock', on_click=saveDefault)
    if lock: st.session_state.edit = False
    if unlock: st.session_state.edit = True

    df = fetch_data()
    ag = AgGrid(df, editable=st.session_state.edit, height=200)
    df2=ag['data']
    st.session_state.store=df2.to_dict()
    st.dataframe(df2)

if __name__ == '__main__':
    app()
    

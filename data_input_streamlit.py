import streamlit as st

your_name = st.text_input("Enter your name", max_chars=10)
st.title(your_name)

number = st.number_input("Enter number", 0, 25, 6, 2)

my_date = st.date_input("Select date") 
st.write(my_date)

vol_1 = st.number_input('Enter vol[mV]')

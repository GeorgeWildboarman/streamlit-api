import streamlit as st

your_name = st.text_input("Enter your name", max_chars=10)
st.title(your_name)

number0 = st.number_input("Enter number")

number1 = st.number_input("Enter number")

number2 = st.number_input("Enter number", 0, 25, 6, 2)

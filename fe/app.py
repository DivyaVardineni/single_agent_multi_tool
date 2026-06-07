import streamlit as st
import requests
import json
import pandas as pd
from decimal import Decimal
import datetime



server_loc="http://127.0.0.1:8000"

w_tab , s_tab , web_tab=st.tabs(["weather Tool","SQL Tool","Web Tool"])

with w_tab:
    st.title("AI Weather Agent")

    city=st.text_input("enter city")
    question=st.text_input("Ask a weather question")

    if st.button("GET"):
        res=requests.post(f"{server_loc}/weather_tooling",params={"city":city,"question":question})
        data=res.json()
        st.write(data["messages"][4]["content"])


with s_tab:
    st.title("SQL Tooling Agent")

    question=st.text_input("enter your Query")

    if st.button("ask SQL"):
        res=requests.post(f"{server_loc}/sql_tooling",params={"question":question})
        data=res.json()
        message=data["messages"][2]["content"]
        #df=pd.DataFrame(message)
        emp = eval(message)
        df = pd.DataFrame(emp)
        st.dataframe(df)

       

with web_tab:
    st.title("Website Tooling Agent")

    question=st.text_input("enter your question ")

    if st.button("ask"):
        res=requests.post(f"{server_loc}/web_tooling",params={"question":question})
        data=res.json()
        st.write(data["messages"][3]["content"])
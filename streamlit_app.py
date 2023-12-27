import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


st.set_page_config(layout="wide")
url = "https://docs.google.com/spreadsheets/d/1T3XQSkstsHXBy2DNs24_y92WWNGu7ihZLzySeU2H8PQ/edit#gid=0"
st.title("DASHBOARD - GCINFRA AGIR")
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=url, usecols=list(range(5)))

st.write("Dados Selecionados:")
st.dataframe(df)


col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col7 = st.columns(2)
col6 = st.columns(1)
col8, col9 = st.columns(2)





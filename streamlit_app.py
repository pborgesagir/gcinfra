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
df1 = conn.read(spreadsheet=url, usecols=list(range(5)))
df = df.sort_values("DATA DE ATRIBUIÇÃO:")

# Convert the "DATA DE ATRIBUIÇÃO:" column to datetime with errors='coerce'
df["DATA DE ATRIBUIÇÃO:"] = pd.to_datetime(df["DATA DE ATRIBUIÇÃO:"], format='%d/%m/%Y', errors='coerce')

# Filter out rows where the date could not be parsed (NaT)
df = df.dropna(subset=["DATA DE ATRIBUIÇÃO:"])

# Extract year, month, and quarter
df["Year"] = df["DATA DE ATRIBUIÇÃO:"].dt.year
df["Month"] = df["DATA DE ATRIBUIÇÃO:"].dt.month
df["Quarter"] = df["DATA DE ATRIBUIÇÃO:"].dt.quarter
df["Semester"] = np.where(df["DATA DE ATRIBUIÇÃO:"].dt.month.isin([1, 2, 3, 4, 5, 6]), 1, 2)

# Create a "Year-Quarter" column
df["Year-Quarter"] = df["Year"].astype(str) + "-T" + df["Quarter"].astype(str)

# If you want to create a "Year-Month" column, you can use the following line
df["Year-Month"] = df["DATA DE ATRIBUIÇÃO:"].dt.strftime("%Y-%m")

# Create a "Year-Quarter" column
df["Year-Semester"] = df["Year"].astype(str) + "-S" + df["Semester"].astype(str)


#----------------------- CREATING THE COLUMN TO DATA DE CONCLUSÃO ------


df = df.sort_values("DATA DE CONCLUSÃO:")
# Convert the "DATA DE ATRIBUIÇÃO:" column to datetime with errors='coerce'
df["DATA DE CONCLUSÃO:"] = pd.to_datetime(df["DATA DE CONCLUSÃO:"], format='%d/%m/%Y', errors='coerce')
# Filter out rows where the date could not be parsed (NaT)
df = df.dropna(subset=["DATA DE CONCLUSÃO:"])

df["Year conclusion"] = df["DATA DE CONCLUSÃO:"].dt.year
df["Month conclusion"] = df["DATA DE CONCLUSÃO:"].dt.month
df["Quarter conclusion"] = df["DATA DE CONCLUSÃO:"].dt.quarter
df["Semester conclusion"] = np.where(df["DATA DE CONCLUSÃO:"].dt.month.isin([1, 2, 3, 4, 5, 6]), 1, 2)

# Create a "Year-Quarter" column
df["Year-Quarter conclusion"] = df["Year conclusion"].astype(str) + "-T" + df["Quarter conclusion"].astype(str)

# If you want to create a "Year-Month" column, you can use the following line
df["Year-Month conclusion"] = df["DATA DE CONCLUSÃO:"].dt.strftime("%Y-%m")

# Create a "Year-Quarter" column
df["Year-Semester conclusion"] = df["Year"].astype(str) + "-S" + df["Semester conclusion"].astype(str)
#--------------------------------------


# Sort the unique values in ascending order
unique_year_month = sorted(df["Year-Month"].unique())
unique_year_quarter = sorted(df["Year-Quarter"].unique())
unique_year_semester = sorted(df["Year-Semester"].unique())
unique_year = sorted(df["Year"].unique())



# Add "All" as an option for both filters
unique_year_month.insert(0, "Todos")
unique_year_quarter.insert(0, "Todos")
unique_year_semester.insert(0, "Todos")
unique_year.insert(0, "Todos")

# Define the list of "CLASSIFICAÇÃO DO PROCESSO:" values and add "Todos" as an option
desired_classificacao = df["CLASSIFICAÇÃO DO PROCESSO:"].unique().tolist()
desired_classificacao.insert(0, "Todos")

# Create a filter for selecting "CLASSIFICAÇÃO DO PROCESSO:"
classificacao = st.sidebar.selectbox("Classificação do Processo:", desired_classificacao)

# Define the list of "NÚMERO DO PROCESSO:" values and add "Todos" as an option
desired_numero_processo = df["NÚMERO DO PROCESSO:"].unique().tolist()
desired_numero_processo.insert(0, "Todos")

# Create a filter for selecting "NÚMERO DO PROCESSO:"
numero_processo = st.sidebar.selectbox("Número do Processo:", desired_numero_processo)




# Create a sidebar for selecting filters
month = st.sidebar.selectbox("Mês", unique_year_month)
quarter = st.sidebar.selectbox("Trimestre", unique_year_quarter)
semester = st.sidebar.selectbox("Semestre", unique_year_semester)
year = st.sidebar.selectbox("Ano", unique_year)


# Define the list of "UNIDADE:" values and add "Todos" as an option
desired_unidades = ["CRER", "HECAD", "HUGOL", "HDS", "AGIR", "TEIA", "CED"]
desired_unidades.insert(0, "Todos")

# Create a filter for selecting "UNIDADE:"
unidade = st.sidebar.selectbox("Unidade:", desired_unidades)

# Check if "All" is selected for the "Year-Month" filter
if month == "Todos":
    month_filtered = df
else:
    month_filtered = df[df["Year-Month"] == month]

# Check if "All" is selected for the "Year-Quarter" filter
if quarter == "Todos":
    filtered_df = month_filtered
else:
    filtered_df = month_filtered[month_filtered["Year-Quarter"] == quarter]


# Check if "All" is selected for the "Year-Quarter" filter
if semester == "Todos":
    filtered_df = filtered_df
else:
    filtered_df = filtered_df[filtered_df["Year-Semester"] == semester]


# Check if "All" is selected for the "Year-Quarter" filter
if year == "Todos":
    filtered_df = filtered_df
else:
    filtered_df = filtered_df[filtered_df["Year"] == year]



# Check if "Todos" is selected for the "UNIDADE:" filter
if unidade != "Todos":
    filtered_df = filtered_df[filtered_df["UNIDADE:"] == unidade]

# Apply filters based on user selection
if classificacao != "Todos":
    filtered_df = filtered_df[filtered_df["CLASSIFICAÇÃO DO PROCESSO:"] == classificacao]

if numero_processo != "Todos":
    filtered_df = filtered_df[filtered_df["NÚMERO DO PROCESSO:"] == numero_processo]
    

# Display the filtered DataFrame
st.write("Dados Selecionados:")
st.dataframe(filtered_df)


col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col7 = st.columns(2)
col6 = st.columns(1)
col8, col9 = st.columns(2)





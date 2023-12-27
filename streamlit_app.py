import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re








st.set_page_config(layout="wide")
url = "https://docs.google.com/spreadsheets/d/1T3XQSkstsHXBy2DNs24_y92WWNGu7ihZLzySeU2H8PQ/edit#gid=0"
st.title("DASHBOARD - GCINFRA AGIR")
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=url, usecols=list(range(7)))
df = df.sort_values("DATA")

# Convert the "DATA" column to datetime with errors='coerce'
df["DATA"] = pd.to_datetime(df["DATA"], format='%d/%m/%Y', errors='coerce')


# Filter out rows where the date could not be parsed (NaT)
df = df.dropna(subset=["DATA"])

# Extract year, month, and quarter
df["Year"] = df["DATA"].dt.year
df["Month"] = df["DATA"].dt.month
df["Quarter"] = df["DATA"].dt.quarter
df["Semester"] = np.where(df["DATA"].dt.month.isin([1, 2, 3, 4, 5, 6]), 1, 2)

# Create a "Year-Quarter" column
df["Year-Quarter"] = df["Year"].astype(str) + "-T" + df["Quarter"].astype(str)

# If you want to create a "Year-Month" column, you can use the following line
df["Year-Month"] = df["DATA"].dt.strftime("%Y-%m")

# Create a "Year-Quarter" column
df["Year-Semester"] = df["Year"].astype(str) + "-S" + df["Semester"].astype(str)



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


# Define the list of "ENTIDADE" values and add "Todos" as an option
desired_classificacao = df["ENTIDADE"].unique().tolist()
desired_classificacao.insert(0, "Todos")

# Create a filter for selecting "ENTIDADE"
classificacao = st.sidebar.selectbox("Entidade", desired_classificacao)

# Define the list of "CLASSIFICAÇÃO" values and add "Todos" as an option
desired_numero_processo = df["CLASSIFICAÇÃO"].unique().tolist()
desired_numero_processo.insert(0, "Todos")

# Create a filter for selecting "CLASSIFICAÇÃO"
numero_processo = st.sidebar.selectbox("Classificação", desired_numero_processo)


# Define the list of "CATEGORIA" values and add "Todos" as an option
categoria = df["CATEGORIA"].unique().tolist()
categoria.insert(0, "Todos")

# Create a filter for selecting "CATEGORIA"
numero_categoria = st.sidebar.selectbox("Categoria", categoria)





# Create a sidebar for selecting filters
month = st.sidebar.selectbox("Mês", unique_year_month)
quarter = st.sidebar.selectbox("Trimestre", unique_year_quarter)
semester = st.sidebar.selectbox("Semestre", unique_year_semester)
year = st.sidebar.selectbox("Ano", unique_year)




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




# Apply filters based on user selection
if classificacao != "Todos":
    filtered_df = filtered_df[filtered_df["ENTIDADE"] == classificacao]

if numero_processo != "Todos":
    filtered_df = filtered_df[filtered_df["CLASSIFICAÇÃO"] == numero_processo]

if numero_categoria != "Todos":
    filtered_df = filtered_df[filtered_df["CATEGORIA"] == numero_categoria]
    

# Display the filtered DataFrame
st.write("Dados Selecionados:")
st.dataframe(filtered_df)




col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)
col9 = st.columns(1)





# Calculate the sum of the "TOTAL BDI (23%)" column
sum_valor_total = filtered_df["TOTAL BDI (23%)"].sum()

# Format the sum to display as Brazilian Real currency
formatted_sum = "R${:,.2f}".format(sum_valor_total)

# Display the sum of "TOTAL BDI (23%)" in a metric display
col1.subheader('Total Valor 💰')
col1.metric(label='Valor Total (R$)', value=formatted_sum, delta=None)

# Count the number of unique values in the "OS" column
unique_marcas_count = filtered_df["OS"].nunique()

# Display the count of unique "MARCA" values in a metric display
col2.subheader('Quantidade de OS 🛠️👷')
col2.metric(label='Número de OS', value=unique_marcas_count, delta=None)



# Function to convert currency strings to float
def currency_to_float(currency):
    # Remove non-numeric characters and convert to float
    return float(re.sub(r'[^\d.]', '', currency))

# Convert 'TOTAL BDI (23%)' column to numeric values
filtered_df['TOTAL BDI (23%)'] = filtered_df['TOTAL BDI (23%)'].apply(currency_to_float)

# Grouping by 'ENTIDADE' and calculating the sum of 'TOTAL BDI (23%)'
grouped_data = filtered_df.groupby('ENTIDADE')['TOTAL BDI (23%)'].sum().reset_index()
grouped_data = grouped_data.sort_values(by='TOTAL BDI (23%)', ascending=False)

# Creating a bar chart using Plotly Express
fig = px.bar(grouped_data, x='ENTIDADE', y='TOTAL BDI (23%)', 
             title='Soma do valor TOTAL BDI (23%) por ENTIDADE',
             labels={'ENTIDADE': 'Entidade', 'TOTAL BDI (23%)': 'Sum of BDI'})
fig.update_layout(xaxis_title='Entidade', yaxis_title='Valor com BDI')

# Display the chart in col1
col3.plotly_chart(fig)




# Chart in col4: Sum of "TOTAL BDI (23%)" grouped by 'CLASSIFICAÇÃO'
grouped_by_classificacao = filtered_df.groupby('CLASSIFICAÇÃO')['TOTAL BDI (23%)'].sum().reset_index()
grouped_by_classificacao = grouped_by_classificacao.sort_values(by='TOTAL BDI (23%)', ascending=False)

fig_classificacao = px.bar(grouped_by_classificacao, x='CLASSIFICAÇÃO', y='TOTAL BDI (23%)',
                           title='Soma do valor TOTAL BDI (23%) por CLASSIFICAÇÃO',
                           labels={'CLASSIFICAÇÃO': 'Classificação', 'TOTAL BDI (23%)': 'Sum of BDI'})
fig_classificacao.update_layout(xaxis_title='Classificação', yaxis_title='Valor com BDI')
col4.plotly_chart(fig_classificacao)



# Grouping by 'CLASSIFICAÇÃO' and calculating the sum of 'TOTAL BDI (23%)'
grouped_by_classificacao_sum = filtered_df.groupby('CLASSIFICAÇÃO')['TOTAL BDI (23%)'].sum().reset_index()

# Creating a pie chart using Plotly Express
fig_classificacao_pie = px.pie(grouped_by_classificacao_sum, values='TOTAL BDI (23%)', names='CLASSIFICAÇÃO',
                              title='Soma do valor TOTAL BDI (23%) por CLASSIFICAÇÃO')
fig_classificacao_pie.update_traces(textposition='inside', textinfo='percent+label')

# Display the pie chart in col3
col5.plotly_chart(fig_classificacao_pie)





# Chart in col5: Sum of "TOTAL BDI (23%)" grouped by 'CATEGORIA'
grouped_by_categoria = filtered_df.groupby('CATEGORIA')['TOTAL BDI (23%)'].sum().reset_index()
grouped_by_categoria = grouped_by_categoria.sort_values(by='TOTAL BDI (23%)', ascending=False)

fig_categoria = px.bar(grouped_by_categoria, x='CATEGORIA', y='TOTAL BDI (23%)',
                       title='Soma do valor TOTAL BDI (23%) por CATEGORIA',
                       labels={'CATEGORIA': 'Categoria', 'TOTAL BDI (23%)': 'Sum of BDI'})
fig_categoria.update_layout(xaxis_title='Categoria', yaxis_title='Valor com BDI')
col6.plotly_chart(fig_categoria)

# Chart in col6: Sum of "TOTAL BDI (23%)" grouped by 'CLASSIFICAÇÃO' and 'ENTIDADE'
grouped_by_class_entidade = filtered_df.groupby(['CLASSIFICAÇÃO', 'ENTIDADE'])['TOTAL BDI (23%)'].sum().reset_index()
grouped_by_class_entidade = grouped_by_class_entidade.sort_values(by='TOTAL BDI (23%)', ascending=False)

fig_class_entidade = px.bar(grouped_by_class_entidade, x='CLASSIFICAÇÃO', y='TOTAL BDI (23%)',
                            color='ENTIDADE',
                            title='Soma do valor TOTAL BDI (23%) por CLASSIFICAÇÃO e ENTIDADE',
                            labels={'CLASSIFICAÇÃO': 'Classificação', 'TOTAL BDI (23%)': 'Sum of BDI'})
fig_class_entidade.update_layout(xaxis_title='Classificação', yaxis_title='Valor com BDI')
col7.plotly_chart(fig_class_entidade)

# Chart in col7: Sum of "TOTAL BDI (23%)" grouped by 'CATEGORIA' and 'ENTIDADE'
grouped_by_cat_entidade = filtered_df.groupby(['CATEGORIA', 'ENTIDADE'])['TOTAL BDI (23%)'].sum().reset_index()
grouped_by_cat_entidade = grouped_by_cat_entidade.sort_values(by='TOTAL BDI (23%)', ascending=False)

fig_cat_entidade = px.bar(grouped_by_cat_entidade, x='CATEGORIA', y='TOTAL BDI (23%)',
                          color='ENTIDADE',
                          title='Soma do valor TOTAL BDI (23%) por CATEGORIA e ENTIDADE',
                          labels={'CATEGORIA': 'Categoria', 'TOTAL BDI (23%)': 'Sum of BDI'})
fig_cat_entidade.update_layout(xaxis_title='Categoria', yaxis_title='Valor com BDI')
col8.plotly_chart(fig_cat_entidade)

# Chart in col8: Line chart summing "TOTAL BDI (23%)" over time
grouped_by_date = filtered_df.groupby('DATA')['TOTAL BDI (23%)'].sum().reset_index()

fig_time = px.line(grouped_by_date, x='DATA', y='TOTAL BDI (23%)',
                   title='Soma do valor TOTAL BDI (23%) ao longo do tempo',
                   labels={'DATA': 'Data', 'TOTAL BDI (23%)': 'Sum of BDI'})
fig_time.update_xaxes(type='date')
fig_time.update_layout(xaxis_title='Data', yaxis_title='Valor com BDI')
st.plotly_chart(fig_time)




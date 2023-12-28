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

# Centered title using HTML tags
st.markdown("<h1 style='text-align: center;'>ANÁLISE DE MEDIÇÕES - MANUTENÇÃO PREDIAL</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

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

classificacao = st.sidebar.multiselect("Unidade", desired_classificacao, default=desired_classificacao[0])

# Define the list of "CLASSIFICAÇÃO" values and add "Todos" as an option
desired_numero_processo = df["CLASSIFICAÇÃO"].unique().tolist()
desired_numero_processo.insert(0, "Todos")

# Create a filter for selecting "CLASSIFICAÇÃO"
numero_processo = st.sidebar.multiselect("Classe", desired_numero_processo, default=desired_numero_processo[0])


# Define the list of "CATEGORIA" values and add "Todos" as an option
categoria = df["CATEGORIA"].unique().tolist()
categoria.insert(0, "Todos")

# Create a filter for selecting "CATEGORIA"
numero_categoria = st.sidebar.multiselect("Subclasse", categoria, default=categoria[0])





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



if classificacao and classificacao != ["Todos"]:
    filtered_df = filtered_df[filtered_df["ENTIDADE"].isin(classificacao)]

if numero_processo and numero_processo != ["Todos"]:
    filtered_df = filtered_df[filtered_df["CLASSIFICAÇÃO"].isin(numero_processo)]

if numero_categoria and numero_categoria != ["Todos"]:
    filtered_df = filtered_df[filtered_df["CATEGORIA"].isin(numero_categoria)]


    




col1, col2, col10 = st.columns(3)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)
col9, col11 = st.columns(2)



# Function to convert currency strings to float
def currency_to_float(currency):
    if isinstance(currency, str):
        # Remove non-numeric characters and convert to float
        return float(re.sub(r'[^\d.]', '', currency))
    elif isinstance(currency, (int, float)):
        # If it's already a number, return it as is
        return float(currency)
    else:
        # Handle other types if necessary
        return None  # You can modify this part based on your specific requirements






# Convert 'TOTAL BDI (23%)' column to numeric values
filtered_df['TOTAL BDI (23%)'] = filtered_df['TOTAL BDI (23%)'].apply(currency_to_float)

# Calculate the sum of the "TOTAL BDI (23%)" column
sum_valor_total = filtered_df["TOTAL BDI (23%)"].sum()

# Format the sum to display as Brazilian Real currency
formatted_sum = "R${:,.2f}".format(sum_valor_total)

# Display the sum of "TOTAL BDI (23%)" in a metric display
col1.subheader('Valor Total 💰')
col1.metric(label='Valor Total (R$)', value=formatted_sum, delta=None)





# Count the number of unique values in the "OS" column
unique_marcas_count = filtered_df["OS"].nunique()

# Display the count of unique "MARCA" values in a metric display
col2.subheader('Quantidade de OS 🛠️👷')
col2.metric(label='Número de OS', value=unique_marcas_count, delta=None)


# Calculate the mean cost of OS and round it to 2 decimal places
mean_cost_os = round(filtered_df["TOTAL BDI (23%)"].sum() / unique_marcas_count, 2)

mean_cost_os = "R${:,.2f}".format(mean_cost_os)

# Display the mean cost of OS in a metric display
col10.subheader('Custo Médio de OS ➗')
col10.metric(label='Custo Médio (R$)', value=mean_cost_os, delta=None)
st.markdown("<br>", unsafe_allow_html=True)





# Convert 'TOTAL BDI (23%)' column to numeric values
filtered_df['TOTAL BDI (23%)'] = filtered_df['TOTAL BDI (23%)'].apply(currency_to_float)

# Grouping by 'ENTIDADE' and calculating the sum of 'TOTAL BDI (23%)'
grouped_data = filtered_df.groupby('ENTIDADE')['TOTAL BDI (23%)'].sum().reset_index()
grouped_data = grouped_data.sort_values(by='TOTAL BDI (23%)', ascending=False)

# Creating a bar chart using Plotly Express
fig = px.bar(grouped_data, x='ENTIDADE', y='TOTAL BDI (23%)', 
             title='Valor por UNIDADE',
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








# Grouping by 'Year-Month' and calculating the sum of 'TOTAL BDI (23%)'
grouped_by_month = filtered_df.groupby('Year-Month')['TOTAL BDI (23%)'].sum().reset_index()

# Calculating the cumulative sum and average
grouped_by_month['Cumulative Sum'] = grouped_by_month['TOTAL BDI (23%)'].cumsum()
grouped_by_month['Cumulative Average'] = grouped_by_month['Cumulative Sum'] / (grouped_by_month.index + 1)

# Filtering the DataFrame for CLASSIFICAÇÃO equal to "M.O.F" or "Outros"
filtered_mof_outros = filtered_df[filtered_df['CLASSIFICAÇÃO'].isin(['M.O.F', 'Outros'])]
grouped_mof_outros = filtered_mof_outros.groupby('Year-Month')['TOTAL BDI (23%)'].sum().reset_index()

# Creating a scatter plot with lines for the sum, cumulative average, and specific CLASSIFICAÇÃO values
fig_monthly_trend = px.scatter(grouped_by_month, x='Year-Month', y='TOTAL BDI (23%)', 
                               title='Tendência do valor TOTAL BDI (23%) por mês',
                               labels={'Year-Month': 'Mês', 'TOTAL BDI (23%)': 'Sum of BDI'})
fig_monthly_trend.add_trace(go.Scatter(x=grouped_by_month['Year-Month'], y=grouped_by_month['TOTAL BDI (23%)'],
                                       mode='lines', name='Soma Mensal'))

fig_monthly_trend.add_trace(go.Scatter(x=grouped_by_month['Year-Month'], y=grouped_by_month['Cumulative Average'],
                                       mode='lines', name='Média Cumulativa'))

fig_monthly_trend.add_trace(go.Scatter(x=grouped_mof_outros['Year-Month'], y=grouped_mof_outros['TOTAL BDI (23%)'],
                                       mode='lines', name='Soma M.O.F/Outros'))

fig_monthly_trend.update_layout(xaxis_title='Mês', yaxis_title='Valor com BDI')
st.plotly_chart(fig_monthly_trend, use_container_width=True)










# Filter the DataFrame for rows where 'CLASSIFICAÇÃO' is 'M.O.F' or 'Outros'
filtered_classificacao = filtered_df[filtered_df['CLASSIFICAÇÃO'].isin(['M.O.F', 'Outros'])]

# Group by 'ENTIDADE' and calculate the sum of 'TOTAL BDI (23%)'
grouped_by_entidade = filtered_classificacao.groupby('ENTIDADE')['TOTAL BDI (23%)'].sum().reset_index()
grouped_by_entidade = grouped_by_entidade.sort_values(by='TOTAL BDI (23%)', ascending=False)

# Create a bar chart using Plotly Express
fig_classificacao_entidade = px.bar(grouped_by_entidade, x='ENTIDADE', y='TOTAL BDI (23%)',
                                    title='Soma do valor TOTAL BDI (23%) para M.O.F e Outros por ENTIDADE',
                                    labels={'ENTIDADE': 'Entidade', 'TOTAL BDI (23%)': 'Sum of BDI'})
fig_classificacao_entidade.update_layout(xaxis_title='Entidade', yaxis_title='Valor com BDI')

# Display the bar chart
col9.plotly_chart(fig_classificacao_entidade)






# Define hospital areas
hospital_areas = {
    "HUGOL": 1500,  # Area of HUGOL in m^2
    "HECAD": 750    # Area of HECAD in m^2
}

# Filter the DataFrame for rows corresponding to each hospital
filtered_hugol = filtered_df[filtered_df['ENTIDADE'] == 'HUGOL']
filtered_hecad = filtered_df[filtered_df['ENTIDADE'] == 'HECAD']

# Calculate the sum of 'TOTAL BDI (23%)' for each hospital
sum_bdi_hugol = filtered_hugol['TOTAL BDI (23%)'].sum()
sum_bdi_hecad = filtered_hecad['TOTAL BDI (23%)'].sum()

# Create a bar chart to display the sums against the respective areas
data = {
    'Hospital': ['HUGOL', 'HECAD'],
    'Total BDI Sum': [sum_bdi_hugol, sum_bdi_hecad],
    'Area (m^2)': [hospital_areas['HUGOL'], hospital_areas['HECAD']]
}

# Create a DataFrame from the data
hospital_data = pd.DataFrame(data)

# Create a bar chart using Plotly Express
fig_hospital_area = px.bar(hospital_data, x='Hospital', y='Total BDI Sum',
                           text='Total BDI Sum', title='Soma do valor TOTAL BDI (23%) por área do hospital',
                           labels={'Hospital': 'Hospital', 'Total BDI Sum': 'Gasto por m^2', 'Area (m^2)': 'Area (m^2)'})

fig_hospital_area.update_traces(texttemplate='%{text:.2s}', textposition='outside')

# Display the bar chart
col11.plotly_chart(fig_hospital_area)












# Display the filtered DataFrame
st.write("Dados Selecionados:")
st.dataframe(filtered_df)



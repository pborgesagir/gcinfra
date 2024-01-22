import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
import streamlit_authenticator as stauth 
import pickle
from pathlib import Path

st.set_page_config(
    page_title='Análise de Medições - Manutenção Predial',
    layout='wide',
    page_icon='🛠️',
    initial_sidebar_state='auto'  
)
#testing authentication
# --- USER AUTHENTICATION ---

names = ["Peter Parker", "Rebecca Miller", "Pedro Borges"]
usernames = ["pparker", "rmiller", "pborges"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=0.00694)

name, authentication_status, username = authenticator.login("Login de acesso: Análise de Medições GCINFRA", "main")

if authentication_status == False:
    st.error("Usuário/senha está incorreto")

if authentication_status == None:
    st.warning("Por favor, insira usuário e senha")

if authentication_status:

#ending authetincation 


    url = "https://docs.google.com/spreadsheets/d/1T3XQSkstsHXBy2DNs24_y92WWNGu7ihZLzySeU2H8PQ/edit#gid=0"
    
    # Centered title using HTML tags
    st.markdown("<h1 style='text-align: center;'>ANÁLISE DE MEDIÇÕES - MANUTENÇÃO PREDIAL</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    
    st.sidebar.image('index.png', width=150)
    
    st.sidebar.title(f"Bem-vindo, {name}")
    
    
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
    
    # Concatenating 'UNIDADE' and 'OS' in'df'
    df["UNIDADE+OS"] = df["UNIDADE"] + '-' + df["OS"]
    
    
    
    
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
    
    
    # Define the list of "UNIDADE" values and add "Todos" as an option
    desired_CLASSE = df["UNIDADE"].unique().tolist()
    desired_CLASSE.insert(0, "Todos")
    
    CLASSE = st.sidebar.multiselect("Unidade", desired_CLASSE, default=desired_CLASSE[0])
    
    # Define the list of "CLASSE" values and add "Todos" as an option
    desired_numero_processo = df["CLASSE"].unique().tolist()
    desired_numero_processo.insert(0, "Todos")
    
    # Create a filter for selecting "CLASSE"
    numero_processo = st.sidebar.multiselect("Classe", desired_numero_processo, default=desired_numero_processo[0])
    
    
    # Define the list of "SUBCLASSE" values and add "Todos" as an option
    SUBCLASSE = df["SUBCLASSE"].unique().tolist()
    SUBCLASSE.insert(0, "Todos")
    
    # Create a filter for selecting "SUBCLASSE"
    numero_SUBCLASSE = st.sidebar.multiselect("Subclasse", SUBCLASSE, default=SUBCLASSE[0])
    
    
    
    
    
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
    
    
    
    if CLASSE and CLASSE != ["Todos"]:
        filtered_df = filtered_df[filtered_df["UNIDADE"].isin(CLASSE)]
    
    if numero_processo and numero_processo != ["Todos"]:
        filtered_df = filtered_df[filtered_df["CLASSE"].isin(numero_processo)]
    
    if numero_SUBCLASSE and numero_SUBCLASSE != ["Todos"]:
        filtered_df = filtered_df[filtered_df["SUBCLASSE"].isin(numero_SUBCLASSE)]
    
    
        
    authenticator.logout("Logout", "sidebar")
    
    
    
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
    
    
    
    
    
    
    # Convert 'TOTAL BDI' column to numeric values
    filtered_df['TOTAL BDI'] = filtered_df['TOTAL BDI'].apply(currency_to_float)
    
    # Calculate the sum of the "TOTAL BDI" column
    sum_valor_total = filtered_df["TOTAL BDI"].sum()
    
    # Format the sum to display as Brazilian Real currency
    formatted_sum = "R${:,.2f}".format(sum_valor_total)
    
    # Display the sum of "TOTAL BDI" in a metric display
    col1.subheader('Valor Total 💰')
    col1.metric(label = '', value=formatted_sum, delta=None)
    
    
    
    
    
    # Count the number of unique values in the "OS" column
    unique_marcas_count = filtered_df["UNIDADE+OS"].nunique()
    
    # Display the count of unique "MARCA" values in a metric display
    col2.subheader('Quantidade de OS 🛠️👷')
    col2.metric(label = '', value=unique_marcas_count, delta=None)
    
    
    # Calculate the mean cost of OS and round it to 2 decimal places
    mean_cost_os = round(filtered_df["TOTAL BDI"].sum() / unique_marcas_count, 2)
    
    mean_cost_os = "R${:,.2f}".format(mean_cost_os)
    
    # Display the mean cost of OS in a metric display
    col10.subheader('Custo Médio de OS ➗')
    col10.metric(label = '', value=mean_cost_os, delta=None)
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    
    
    
    # Convert 'TOTAL BDI' column to numeric values
    filtered_df['TOTAL BDI'] = filtered_df['TOTAL BDI'].apply(currency_to_float)
    
    # Grouping by 'UNIDADE' and calculating the sum of 'TOTAL BDI'
    grouped_data = filtered_df.groupby('UNIDADE')['TOTAL BDI'].sum().reset_index()
    grouped_data = grouped_data.sort_values(by='TOTAL BDI', ascending=False)
    
    # Creating a bar chart using Plotly Express
    fig = px.bar(grouped_data, x='UNIDADE', y='TOTAL BDI', 
                 title='VALOR POR UNIDADE',
                 labels={'UNIDADE': 'Unidade', 'TOTAL BDI': 'Valor com BDI'})
    fig.update_layout(xaxis_title='Unidade', yaxis_title='Valor com BDI')
    
    # Display the chart in col1
    col3.plotly_chart(fig)
    
    
    
    
    # Chart in col4: Sum of "TOTAL BDI" grouped by 'CLASSE'
    grouped_by_CLASSE = filtered_df.groupby('CLASSE')['TOTAL BDI'].sum().reset_index()
    grouped_by_CLASSE = grouped_by_CLASSE.sort_values(by='TOTAL BDI', ascending=False)
    
    fig_CLASSE = px.bar(grouped_by_CLASSE, x='CLASSE', y='TOTAL BDI',
                               title='VALOR POR CLASSE',
                               labels={'CLASSE': 'Classe', 'TOTAL BDI': 'Valor com BDI'})
    fig_CLASSE.update_layout(xaxis_title='Classe', yaxis_title='Valor com BDI')
    col4.plotly_chart(fig_CLASSE)
    
    
    
    # Grouping by 'CLASSE' and calculating the sum of 'TOTAL BDI'
    grouped_by_CLASSE_sum = filtered_df.groupby('CLASSE')['TOTAL BDI'].sum().reset_index()
    
    # Creating a pie chart using Plotly Express
    fig_CLASSE_pie = px.pie(grouped_by_CLASSE_sum, values='TOTAL BDI', names='CLASSE',
                                  title='PERCENTUAL POR CLASSE')
    fig_CLASSE_pie.update_traces(textposition='inside', textinfo='percent+label')
    
    # Display the pie chart in col3
    col5.plotly_chart(fig_CLASSE_pie)
    
    
    
    
    
    # Chart in col5: Sum of "TOTAL BDI" grouped by 'SUBCLASSE'
    grouped_by_SUBCLASSE = filtered_df.groupby('SUBCLASSE')['TOTAL BDI'].sum().reset_index()
    grouped_by_SUBCLASSE = grouped_by_SUBCLASSE.sort_values(by='TOTAL BDI', ascending=False)
    
    fig_SUBCLASSE = px.bar(grouped_by_SUBCLASSE, x='SUBCLASSE', y='TOTAL BDI',
                           title='VALOR POR SUBCLASSE',
                           labels={'SUBCLASSE': 'Subclasse', 'TOTAL BDI': 'Valor com BDI'})
    fig_SUBCLASSE.update_layout(xaxis_title='Subclasse', yaxis_title='Valor com BDI')
    col6.plotly_chart(fig_SUBCLASSE)
    
    # Chart in col6: Sum of "TOTAL BDI" grouped by 'CLASSE' and 'UNIDADE'
    grouped_by_class_UNIDADE = filtered_df.groupby(['CLASSE', 'UNIDADE'])['TOTAL BDI'].sum().reset_index()
    grouped_by_class_UNIDADE = grouped_by_class_UNIDADE.sort_values(by='TOTAL BDI', ascending=False)
    
    fig_class_UNIDADE = px.bar(grouped_by_class_UNIDADE, x='CLASSE', y='TOTAL BDI',
                                color='UNIDADE',
                                title='BENCHMARKING POR CLASSE',
                                labels={'CLASSE': 'CLASSE', 'TOTAL BDI': 'Sum of BDI'})
    fig_class_UNIDADE.update_layout(xaxis_title='Classe', yaxis_title='Valor com BDI')
    col7.plotly_chart(fig_class_UNIDADE)
    
    # Chart in col7: Sum of "TOTAL BDI" grouped by 'SUBCLASSE' and 'UNIDADE'
    grouped_by_cat_UNIDADE = filtered_df.groupby(['SUBCLASSE', 'UNIDADE'])['TOTAL BDI'].sum().reset_index()
    grouped_by_cat_UNIDADE = grouped_by_cat_UNIDADE.sort_values(by='TOTAL BDI', ascending=False)
    
    fig_cat_UNIDADE = px.bar(grouped_by_cat_UNIDADE, x='SUBCLASSE', y='TOTAL BDI',
                              color='UNIDADE',
                              title='BENCHMARKING POR SUBCLASSE',
                              labels={'SUBCLASSE': 'Subclasse', 'TOTAL BDI': 'Valor com BDI'})
    fig_cat_UNIDADE.update_layout(xaxis_title='Subclasse', yaxis_title='Valor com BDI')
    col8.plotly_chart(fig_cat_UNIDADE)
    
    
    
    
    
    
    
    
    # Grouping by 'Year-Month' and calculating the sum of 'TOTAL BDI'
    grouped_by_month = filtered_df.groupby('Year-Month')['TOTAL BDI'].sum().reset_index()
    
    # Calculating the cumulative sum and average
    grouped_by_month['Cumulative Sum'] = grouped_by_month['TOTAL BDI'].cumsum()
    grouped_by_month['Cumulative Average'] = grouped_by_month['Cumulative Sum'] / (grouped_by_month.index + 1)
    
    # Filtering the DataFrame for CLASSE equal to "M.O.F" or "Outros"
    filtered_mof_outros = filtered_df[filtered_df['CLASSE'].isin(['M.O.F', 'Outros'])]
    grouped_mof_outros = filtered_mof_outros.groupby('Year-Month')['TOTAL BDI'].sum().reset_index()
    
    # Creating a scatter plot with lines for the sum, cumulative average, and specific CLASSE values
    fig_monthly_trend = px.scatter(grouped_by_month, x='Year-Month', y='TOTAL BDI', 
                                   title='ACOMPANHAMENTO AO LONGO DO TEMPO',
                                   labels={'Year-Month': 'Mês', 'TOTAL BDI': 'Sum of BDI'})
    fig_monthly_trend.add_trace(go.Scatter(x=grouped_by_month['Year-Month'], y=grouped_by_month['TOTAL BDI'],
                                           mode='lines', name='Soma Mensal'))
    
    fig_monthly_trend.add_trace(go.Scatter(x=grouped_by_month['Year-Month'], y=grouped_by_month['Cumulative Average'],
                                           mode='lines', name='Média Cumulativa'))
    
    fig_monthly_trend.add_trace(go.Scatter(x=grouped_mof_outros['Year-Month'], y=grouped_mof_outros['TOTAL BDI'],
                                           mode='lines', name='M.O.F + Outros'))
    
    fig_monthly_trend.update_layout(xaxis_title='Mês', yaxis_title='Valor com BDI')
    st.plotly_chart(fig_monthly_trend, use_container_width=True)
    
    
    
    
    
    
    
    
    
    
    # Filter the DataFrame for rows where 'CLASSE' is 'M.O.F' or 'Outros'
    filtered_CLASSE = filtered_df[filtered_df['CLASSE'].isin(['M.O.F', 'Outros'])]
    
    # Group by 'UNIDADE' and calculate the sum of 'TOTAL BDI'
    grouped_by_UNIDADE = filtered_CLASSE.groupby('UNIDADE')['TOTAL BDI'].sum().reset_index()
    grouped_by_UNIDADE = grouped_by_UNIDADE.sort_values(by='TOTAL BDI', ascending=False)
    
    # Create a bar chart using Plotly Express
    fig_CLASSE_UNIDADE = px.bar(grouped_by_UNIDADE, x='UNIDADE', y='TOTAL BDI',
                                        title='VALOR PARA M.O.F + OUTROS POR UNIDADE',
                                        labels={'UNIDADE': 'Unidade', 'TOTAL BDI': 'Soma com BDI'})
    fig_CLASSE_UNIDADE.update_layout(xaxis_title='Unidade', yaxis_title='Valor com BDI')
    
    # Display the bar chart
    col9.plotly_chart(fig_CLASSE_UNIDADE)
    
    
    
    
    
    
    # Define hospital areas
    hospital_areas = {
        "HUGOL": 55105,  # Area of HUGOL in m^2
        "HECAD": 24520,  # Area of HECAD in m^2
        "CRER": 33275,   # Area of CRER in m^2
        "HDS": 4257      # Area of HDS in m^2
    }
    
    # Group by 'UNIDADE' and calculate the total sum of 'TOTAL BDI' for each hospital
    grouped_by_hospital = filtered_df.groupby('UNIDADE')['TOTAL BDI'].sum().reset_index()
    
    # Group by 'UNIDADE' and 'Year-Month' to count the number of months for each hospital
    months_per_hospital = filtered_df.groupby(['UNIDADE', 'Year-Month']).size().groupby('UNIDADE').size().reset_index(name='NumMonths')
    
    # Merge the total sum and number of months per hospital
    grouped_by_hospital = grouped_by_hospital.merge(months_per_hospital, on='UNIDADE')
    
    # Calculate spending per square meter for each hospital
    for hospital, area in hospital_areas.items():
        mask = grouped_by_hospital['UNIDADE'] == hospital
        grouped_by_hospital.loc[mask, 'Spending per m^2'] = grouped_by_hospital[mask]['TOTAL BDI'] / (area * grouped_by_hospital[mask]['NumMonths'])
    
    # Create a bar chart to display average spending per square meter for each hospital
    fig_hospital_avg_spending_per_m2 = px.bar(grouped_by_hospital, x='UNIDADE', y='Spending per m^2',
                                              title='GASTO MÉDIO POR M^2',
                                              labels={'UNIDADE': 'Hospital', 'Spending per m^2': 'Gasto médio por m^2'})
    fig_hospital_avg_spending_per_m2.update_layout(xaxis_title='Hospital', yaxis_title='Gasto médio por m^2')
    
    # Display the bar chart
    col11.plotly_chart(fig_hospital_avg_spending_per_m2)
    
    
    #######################  TESTING ADDING SANKEY DIAGRAM
    # Grouping by 'CLASSE', 'SUBCLASSE', and calculating the sum of 'TOTAL BDI'
    grouped_by_class_subclass = filtered_df.groupby(['CLASSE', 'SUBCLASSE'])['TOTAL BDI'].sum().reset_index()
    
    # Create a Sankey diagram using Plotly Express
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=grouped_by_class_subclass['CLASSE'].unique().tolist() + grouped_by_class_subclass['SUBCLASSE'].unique().tolist()
        ),
        link=dict(
            source=grouped_by_class_subclass['CLASSE'].map(lambda x: np.where(grouped_by_class_subclass['CLASSE'].unique() == x)[0][0]),
            target=len(grouped_by_class_subclass['CLASSE'].unique()) + grouped_by_class_subclass['SUBCLASSE'].map(lambda x: np.where(grouped_by_class_subclass['SUBCLASSE'].unique() == x)[0][0]),
            value=grouped_by_class_subclass['TOTAL BDI']
        )
    )])
    
    # Update the layout of the Sankey diagram
    fig_sankey.update_layout(title_text="Diagrama de Sankey - Distribuição Valor Total por Classe e Subclasse",
                            font_size=10,
                            width=800,
                            height=600)
    
    # Display the Sankey diagram
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    
    ######### END OF TESTING
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Display the filtered DataFrame
    st.write("Dados Selecionados:")
    st.dataframe(filtered_df)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    link = "https://docs.google.com/forms/d/e/1FAIpQLSdv3CkTWlm_DlmIthQkFwAyopnu9lelO-jKjPrTcJ0ZLOXmqQ/viewform"
    text = "<h2 style='text-align: center; font-size: 18px;'><a href='{}' target='_blank'>Clique aqui para acessar o formulário de envio das planilhas de medições</a></h2>".format(link)
    
    st.markdown(text, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    
    
    
    






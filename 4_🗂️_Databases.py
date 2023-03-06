import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
from pandas.io.json import json_normalize
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


#st.title("📈 Select the relevant database to estimate emissions")
st.markdown("<h1 style='text-align:center; font-family: Roboto;'>📈 Select the database 📈</h1>", unsafe_allow_html=True)
#st.markdown("<h1 style='text-align:center'>📈 Select the database</h1>", unsafe_allow_html=True)

st.markdown("""---""")

col1, col2, col3 = st.columns(3)
with col1:
    climatiq = st.checkbox('🗂️ Climatiq database')
    if climatiq:
        st.write('Climatic database selected')

with col2:
    eco = st.checkbox('🗂️ Eco-invent database')
    if eco:
        st.write('Eco-invent database selected')
        
with col3:
    ademe = st.checkbox(' 🗂️ Ademe Base database')
    if ademe:
        st.write('Ademe Base Carbone database selected')
        
##################################################################################################
Auth = 'Authorization: Bearer <API_KEY>'   # Always provide an authentication token which is supplied by the website.
url = 'https://beta3.api.climatiq.io/estimate'  # This is the endpoint
headers = {"Authorization": "Bearer NBGNH8EMD44XK9GP67KSPP1HTXB6"}
#################################################################################################

# Activity data and emission factor selection are bundled together # 
countries = ['FR', 'US'] 
database =['ADEME', 'BEIS', 'EPA']
year = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
category = ['Electricity']      

with st.form("compute"):
    st.write("Insert your query parameters")
    category = st.selectbox('Activity category', category)
    value = float(st.text_input("value", value="0"))
    energy_unit = st.selectbox("Energy Unit:", ["kWh", "MJ", "GWh"])
    country  = st.selectbox('Country selection', countries)
    emission_factor_source = st.selectbox ('Select database', database)
    year = st.selectbox('Select year', year)
    submit = st.form_submit_button("Submit Query")
if submit:
    parameters = {
    "energy": value,
    "energy_unit": energy_unit
    }
    # You can actually widen the emission factor selection criteria
    data = {
    "emission_factor": {
        "source": emission_factor_source,
        "year": year,
        'region': country,
        'category': category
    },
    # Specify how much energy we're estimating for
    "parameters": parameters
    }
    response = requests.post(url, params = data, headers=headers, json = data)
    status_code =print(response.status_code)
    data =response.json()
    df1 = pd.json_normalize(response.json())
    st.table(df1.T)

        
        
        



    
    

    
    

    


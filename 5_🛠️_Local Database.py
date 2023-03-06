import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import altair as alt
import math

st.markdown("<h1 style='text-align:center; font-family: Roboto;'> 🌎 Co2 Estimator </h1>", unsafe_allow_html=True)
st.markdown("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
# Read in the database from Github
url = 'https://raw.githubusercontent.com/Brilla1234/My-Datasets/main/emission_factors_long.csv'
df = pd.read_csv(url)
df.index.names = ['Row_ID']
df['Year'] = df['Year'].astype('int')

#Add pagination to data
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gridOptions = gb.build()

show_database = st.checkbox('Display Database')
if show_database:
    st.header('Electricity Emission Factors (gC02e/Kwh)')
    AgGrid(df, gridOptions=gridOptions)

# Input selection and filtering
selected_country = st.selectbox('Select a country', df['Country'].unique())
selected_year = st.slider('Select a year', 2018, 2023, step =1)
activity_data = st.number_input('Electricity purchased(kwh)')

per = [f"{i}%" for i in range(0, 110, 10)]

#print("Min value:", per[0])
#print("Max value:", per[-1])
with st.sidebar:
    st.header('Select uncertainty percentages')
    uncertainty_data = st.slider('Activity data(%)', 0, 100, step =1)
    uncertainty_emission = st.slider('Emission factor(%)', 0,100, step =1)
    
   

st.markdown("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; font-family: Roboto;'> Results </h1>", unsafe_allow_html=True)
# Emission factor value
result = df.loc[(df.Country == selected_country) & (df.Year == selected_year)]
#st.write(result)
emission_factor = (result.iloc[0]['Emission_factor'])

col1, col2, col3 = st.columns(3)
with col1:
    st.write('The emission factor value in gCo2e/kWh is:')
    st.header(emission_factor) 
    data = {"emission factor": [emission_factor]}
    df = pd.DataFrame(data)
    df_long = df.melt(var_name="Category", value_name="Value")
    df1_long = df_long.sort_values(by =['Value'], ascending = False)
    fig =alt.Chart(df1_long, title ='Emission factor').mark_bar().encode(y ='Value')
    st.altair_chart(fig, use_container_width=True, theme ='streamlit')

with col2:
    st.write('The total emissions in gCo2e are:')
    Co2_emission = activity_data * (emission_factor)
    st.header(Co2_emission)
    data = {"Total emission": [Co2_emission]}
    df = pd.DataFrame(data)
    df_long = df.melt(var_name="Category", value_name="Value")
    df1_long = df_long.sort_values(by =['Value'], ascending = False)
    fig =alt.Chart(df1_long, title ='Total emissions').mark_bar().encode(y ='Value')
    st.altair_chart(fig, use_container_width=True, theme ='streamlit')
with col3:
    st.write('The total emissions in KgCo2e are:')
    result_kg = Co2_emission/(1000)
    st.header(result_kg)
    data = {"Total emission": [result_kg]}
    df = pd.DataFrame(data)
    df_long = df.melt(var_name="Category", value_name="Value")
    df1_long = df_long.sort_values(by =['Value'], ascending = False)
    fig =alt.Chart(df1_long, title ='Total emissions').mark_bar().encode(y ='Value')
    st.altair_chart(fig, use_container_width=True, theme ='streamlit')

# We use the math module in python to write a backward error propagation formula
#Uncertainty values are extracted from sliders
k = (activity_data*(uncertainty_data/100))**2 + (emission_factor*(uncertainty_emission/100))**2
c = k / (uncertainty_data + uncertainty_emission)
value = round(math.sqrt(c),2) # Uncertainty value

string = str(value) + ' ' + '+/-%'
st.header('The overall uncertainty is:')
st.header(string)

# I use the estimated uncertainty to create add_on
add_on = Co2_emission * (value/100)

#add_on is added to and subtracted from total emission value to generate confidence rage
max_value  = Co2_emission + add_on
min_value = Co2_emission - add_on

max = str(round(max_value,2))
min = str(round(min_value,2))

st.header('The confidence range is:')
range = min + '-' + max
st.header(range)


st.write(st.session_state.country)
st.write(st.session_state.site_name)
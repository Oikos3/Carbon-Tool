#Import libraries & Frameworks
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import altair as alt
import math
from streamlit_option_menu import option_menu
import plotly.express as px
import datetime
#################################


# PAGE CONFIGURATION AND TITLES
st.set_page_config(
     page_title="Eolos OIKOS_3",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded")

st.info('This is a purely informational message', icon="ℹ️")
#Reduce top space in the streamlit application
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

#Header of the page
st.markdown("<h1 style='text-align: center; color: rgb(185,91,61); font-family: Arial; font-size: 40px; background-color:#f0f2f6; border-radius: 10px; padding: 20px;'> Multi-Site Scope 2 Estimations  </h1>", unsafe_allow_html=True)
st.markdown("""---""")


#Read in the database and try to cache the database with the cache decorator
@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    df = pd.read_csv(url)
    return df
url = 'https://raw.githubusercontent.com/Brilla1234/My-Datasets/main/database_elec.csv'
df = load_data(url)
df['Year'] = df['Year'].astype('int') #Year is changed to an integer value

#Add pagination to the database and create table using AGGRID
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_pagination()
gridOptions = gb.build()

# SET THE COUNTRY AND SITE MAPPINGS AT THIS STAGE. we write a set of inputs and use forloop to generate cells
st.markdown("<h1 style='text-align: center; color: black; background-color:#f0f2f6; font-family: Arial; border-radius: 8px; font-size: 30px;'> 🛠️ Parameter Settings  </h1>", unsafe_allow_html=True)

# Add ability to add start and end date of the reporting
col1, col2, col3, col4 = st.columns(4)
with col1: # Start date
    d = st.date_input(
    "Start date",
    datetime.date(2019,7,6))

with col2: # End date
    d = st.date_input(
    "End date",
    datetime.date(2019,7,6))


with col3:
    company_turnover = st.number_input('Company Turnover(€)',  min_value=100, key='tehm')

with col4:
    company_fte = st.number_input('Company FTE', min_value=1, key='tem')

# Map countries to sites
with st.expander('Click to map countries to their sites'):
    col4, col5, col6 = st.columns(3)
    with col4:
        pass
    with col5:
        value = st.number_input('Enter # of Sites', value =1, min_value=1, key='love') 
    with col6:
        pass
    cola, colb = st.columns(2)
    with cola:
        st.write('Country')
    with colb:
        st.write('Site')   
    def mapper(k):
        col1, col2 = st.columns(2)
        with col1:
            #st.write('country')
            country = st.selectbox('Select a country', df['Country'].unique(), label_visibility = 'collapsed', key=f'country_{k}') # The country name here is derived from the database as selection
            #country = st.selectbox('Select a country', df['Country'].unique(),key=f'3_{t}' )
        with col2:
            site_param = st.text_input(f'site', label_visibility = 'collapsed', key=f'site_name_{k}')
        return country, site_param

    def collect_data(value):
        data = []
        for i in range(value):
            parameters = mapper(i)
            data.append(parameters)   
        df = pd.DataFrame(data, columns=['Country','Site name'])
        return df
    num_of_sites = value
    df_1 = collect_data(num_of_sites)
    load_table = st.checkbox('Load table')
    if load_table:
        AgGrid(df_1)


    #st.dataframe(df_1)
###############################################################

#Initialize 3 columns to contain the initialization parameters such as activities, year and site binding.
col1, col2, col3 = st.columns(3)
with col1: # Define the number of times a cell should be generated
    value = st.number_input('Enter # of Activities', value =1, min_value=1) 
    number = value    
with col2:
    pass
with col3:
    year = st.slider('Select accounting year for emission values', 2018, 2022, step=1) # Define year for emission factor

#Display Database now
show_database = st.checkbox('Display Database')
if show_database:
    st.markdown("<h1 style='text-align: center; color: black; font-family: Arial; font-size: 30px;'> 🗂️ Electricity Emission Factors (tC02e/Kwh) 🗂️ </h1>", unsafe_allow_html=True)
    #st.header('Electricity Emission Factors (tC02e/Kwh)')
    AgGrid(df, gridOptions=gridOptions)
st.markdown("""---""")


# Define the input parameters for a specific activity related to carbon emissions
#The category label heplps us to refine the activity description
category_label = ['1-1 Direct emissions from electricity consumption',
'1-2 Direct emissions from mobile sources with combustion',
'1-3 Direct emissions from processes',
'1-4 Direct fugitive emissions',
'1-5 Indirect emissions from electricity consumption',
'1-6 Indirect emissions from steam, heat or cooling consumption']

#Placeholders for entering data into the system
#For market and location based 
st.markdown("<h1 style='text-align: center; color: black; background-color:#f0f2f6; font-family: Arial; border-radius: 8px; font-size: 30px;'> 🗒️ Data Entry  </h1>", unsafe_allow_html=True)
st.markdown("""---""")
emission_factor_market = None # We set a global variable
def site(t):
    global emission_factor_market
    country = st.selectbox('Select a country', df_1['Country'].unique(),key=f'3_{t}' )
    df_2 = df_1[df_1['Country'] == country]  # We filter by country to enable us to display sites mapped to a specific country
    #site_name = st.selectbox(f'Site name :', df_1['Site name'].unique(), key=f'2_{t}')
    site_name = st.selectbox(f'Site name :', df_2['Site name'].unique(), key=f'2_{t}')
    # Enable toggle between market & Location based emission factors
    result = df.loc[(df.Country == country) & (df.Year == year)]  # filtering to enable emission factor selection
    emission_factor = (result.iloc[0]['Emission_factor'])
    market_factor = st.checkbox('Click to add market estimate', key = f'44_{t}')
    a = 0
    if market_factor:
       emission_factor_market = (result.iloc[0]['Emission_factor_market'])
    else:
        emission_factor_market = a
    uncertainty_value_factor = (result.iloc[0]['Uncertainty_Value'])

    #Continue with inputs
    activity_description = st.text_input(f'Description of activity:', key=f'4_{t}')
    category = st.selectbox('Select category:', category_label, key=f'50_{t}')
    activity_value = float(st.text_input('Activity data', value="0",key=f'5_{t}'))
    activity_unit = st.selectbox('Unit', ['kWh'], key=f'10_{t}')
    uncertainty_value = float(st.text_input('Uncertainty value of activity data(%)', value="0",key=f'6_{t}'))

    #uncertainty_used = uncertainty_value/100 #  uncertain value for activity used in calculation
    #Calculate emission values to be returned as part of the dataframe.
    total_emission = activity_value * emission_factor
    total_emission_market = activity_value * emission_factor_market
    #calculate final uncertainty value
    total_uncertainty = (activity_value * uncertainty_value)**2 + (emission_factor * uncertainty_value_factor)**2
    c = math.sqrt(total_uncertainty) # Uncertainty value
    d = round(c / (activity_value + emission_factor),2)
    value = d # Uncertainty value
    return country, site_name, emission_factor, uncertainty_value_factor, activity_description,category, activity_value, activity_unit, uncertainty_value, total_emission, value, emission_factor_market, total_emission_market

#emission factor selection criteria:
# Use a foreloop to generate cells based on the entered activity data.
def collect_data(number):
    data = []
    for i in range(number):
        with st.expander('Activity details'):
            site_data = site(i)
        data.append(site_data)    
    df = pd.DataFrame(data, columns=['Country', 'Site Name','Emission Factor', 'Uncertainty_Value(factor)', 'Activity Description','Activity Category', 'Activity Value', 'Activity Unit', 'Uncertainty Value(data)', 'Total Emissions(tCO2e)', 'Total Uncertainty', 'Emission Factor(market)', 'Total Emissions Market(tCO2e)'])
    return df

num_of_sites = number


df = collect_data(num_of_sites)
load_dataframe = st.checkbox('Load excel report')
if load_dataframe:
    AgGrid(df)

#st.table(df)
#AgGrid(df)



#Start generating results using table
#st.markdown("<h1 style='text-align: center; color: black; font-family: Arial; font-size: 30px;'> 📈 RESULTS 📈</h1>", unsafe_allow_html=True)
#st.markdown("<h1 style='text-align: center; color: black; background-color: #ff4b4b; font-family: Arial; font-size: 30px;'> 📈 RESULTS 📈</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: black; background-color:#f0f2f6; font-family: Arial; font-size: 30px; border-radius: 8px;'> 📊 Dashboard 📊  </h1>", unsafe_allow_html=True)
st.markdown("""---""")

# Non_graph Total Results
Total_emissions = df['Total Emissions(tCO2e)'].sum()
Total_emissions = round(Total_emissions, 0)
Total_emissions = str(Total_emissions)+ ' ' + 'tCO2e'

# Non_graph Average Results
Average_emissions = df['Total Emissions(tCO2e)'].mean()
Average_emissions = round(Average_emissions, 0)
Average_emissions = str(Average_emissions)+ ' ' + 'tCO2e'

# Non graph uncertainty results
Rel_Uncertainty = df['Total Uncertainty'].mean()
Rel_Uncertainty = round(Rel_Uncertainty, 0)
Rel_Uncertainty = str(Rel_Uncertainty)+ ' ' + '%'


col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<h1 style='text-align: left; color: black; font-family:Sans serif; font-size: 20px; border-radius: 8px;'> 📈 Average Emissions </h1>", unsafe_allow_html=True)
    st.subheader(Average_emissions)

with col2:
    st.markdown("<h1 style='text-align: left; color: black; font-family:Sans serif; font-size: 20px; border-radius: 8px;'> 📈 Total Emissions </h1>", unsafe_allow_html=True)
    st.subheader(Total_emissions)

with col3:
    st.markdown("<h1 style='text-align: left; color: black; font-family:Sans serif; font-size: 20px; border-radius: 8px;'> 📈 Relative Uncertainty </h1>", unsafe_allow_html=True)
    st.subheader(Rel_Uncertainty)

#  GROUPBYS
df_country = df.groupby('Country')['Total Emissions(tCO2e)'].sum().sort_values(ascending=False).reset_index() #country groupby
df_site = df.groupby(['Country', 'Site Name'])['Total Emissions(tCO2e)'].sum().sort_values(ascending=False).reset_index() #site groupby
df_ac = df.groupby('Activity Description')['Total Emissions(tCO2e)'].sum().sort_values(ascending=False).reset_index() #activity groupby
# df is your raw unaggregated dataframe
# Bar Chart
st.markdown("""---""")
fig =alt.Chart(df_country.sort_values(by='Total Emissions(tCO2e)', ascending=False), 
               title ='Emissions By Country').mark_bar().encode(
  x ='Total Emissions(tCO2e)', 
  y = alt.Y('Country', sort='-x'),
  color = 'Country'
)
st.altair_chart(fig, use_container_width=True)

#Country and site level emissions
fig =alt.Chart(df_site.sort_values(by='Total Emissions(tCO2e)', ascending=False), 
               title ='Emissions By Country and Site').mark_bar().encode(
  x ='Total Emissions(tCO2e)', 
  y = alt.Y('Country', sort='-x'),
  color = 'Site Name'
)
st.altair_chart(fig, use_container_width=True)



col1, col2 = st.columns(2)
with col1:
    st.markdown("""---""")
    
# Pie Chart
    fig1 =alt.Chart(df_ac, title = 'Emissions by Activity').mark_arc().encode(
    theta=alt.Theta(field="Total Emissions(tCO2e)", type="quantitative"),
    color=alt.Color(field="Activity Description", type="nominal"),
    )
    st.altair_chart(fig1, use_container_width=True, theme ='streamlit')



with col2:
    fig = px.pie(df, values='Total Emissions(tCO2e)', names='Activity Description', hole=.3)
    st.plotly_chart(fig)





#with col2:
#    fig =alt.Chart(df, title ='Emission factor').mark_bar().encode(y ='Activity Value', x = 'Activity Description', color = 'Activity Description')
#    st.altair_chart(fig, use_container_width=True)

#st.markdown("<div style='background-color: ; padding: 50px;'>Your content here</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header('Dashboard filters')
    options = st.multiselect(
    'SELECT TO DISPLAY',
    ['Emissions by Country',
     'Emissions by Country & Site', 
     'Emissions by Activity', 
     'Emissions by Activity, Site & Country)'])


# SESSION STATE

st.write(st.session_state)

# Hide streamlit logo
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



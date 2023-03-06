import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


#WEB PAGE CONFIGURATION
st.set_page_config(page_title = "Carbon Writer",layout = 'wide')  # you can add the argument layout = "wide"

# Define a function that extracts  animation from lottie files
def load_lottieurl(url):
    r =requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()   
# lottie = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_2p5ywtpt.json")
# st_lottie(lottie, key ='covid')   
    
      
# Connect a style sheet to the streamlit file with the code below        
# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    
with st.expander("Go to the homepage to learn more about the eolos carbon tool"):
    st.write('This tool is a beta version and the functionalities are currently being tested')
    st.write('Version 202212.12')

#col1,  = st.column(2)
#with col1:
    st.markdown("<h1 style='text-align: left; color: black; font-family: Arial; font-size: 20px;'>Eolos Carbon Calculator</h1>", unsafe_allow_html=True)
    
#with col2:
    #image = Image.open(r'C:\Users\Nana\Carbon\eolos image.jpg')
    #new = image.resize((400, 100))
    #st.image(new)
              

# Add a sidebar and select type of emission scope from sidebar
#with st.sidebar:
#     image = Image.open(r'C:\Users\Nana\eolos image.jpg')
#     new = image.resize((400,100))                  
#     st.image(new)
    
    st.markdown("### Emission Scope Filter")
    add_selectbox = st.sidebar.selectbox(
    "Select the emission scope",
    ("Scope 1", "Scope 2", "Scope 3")
    )
# Rule a line
    st.markdown("""---""")
# Add the choice to select the industry
    st.markdown("### Emission Sources Filter")

    add_radio = st.radio(
       "Click to select the source",
       ("Energy", "Non-Energy", "Input 1", "Manufacturing",'Direct Waste', 'Packaging','Freight', 'Transport')
)
    

    
#Accepts an Excel or CSV file (The function first tries to read the file as an excel if it doesn't work, it reads the file as a csv)
# I define df as a global variable so that I can access it outside the function.
#######################################################################################################
df = None


def load_data():
    files = st.file_uploader('Choose your excel or csv file', accept_multiple_files = True)
    for file in files:
        global df
        try:
            df = pd.read_excel(file)
        except:
            df = pd.read_csv(file)    
        if st.checkbox('View full data'):
            #st.dataframe(df, use_container_width=True)
            AgGrid(df.head(100))
load_data()
#########################################################################################################
# Have to invoke this anytime you call a df outside the function.
# This code allows the user to select specific columns and perform arithmetic operations

# Data summarizer
if df is not None:
    summarize = st.checkbox('summarize data')
    if summarize:
      a = df.describe()
      b =a.round(1)
      st.table(b)                  
                        
                     

if df is not None:
    col1, col2, col3 = st.columns(3)
    with col1:
        col1 = st.selectbox('Select the first column', df.columns)
    with col2:
        col2 = st.selectbox('Select the second column', df.columns)
    with col3:
        operation = st.selectbox('Select an operation', ['+', '-', 'x','/'])    
    if operation == '+':
        df['result'] = df[col1] + df[col2]  
    elif operation == '-':
        df['result'] = df[col1] - df[col2]
    elif operation == 'x':
        df['result'] = df[col1] * df[col2]
    elif operation == '/':
        df['result'] = df[col1] / df[col2]
    st.dataframe(df) 
        

# ENERGY 1 COMPUTATIONS
if add_radio == 'Energy':
    st.subheader('Energy values')
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            value1 = float(st.text_input("Fuels, direct accounting", value="0"))
            value2 = float(st.text_input(label="Fossil fuel heating, estimated", value="0"))
            value3 = float(st.text_input(label="Steam purchased", value="0"))
            value4 = float(st.text_input(label="Cooling purchased", value="0"))
            value5= float(st.text_input(label="Electricity, purchased & produced", value="0"))
#             value1 =st.number_input('Fuels, direct accounting', key ='value1')
#             value2 =st.number_input('Fossil fuel heating, estimated', key ='value2')
#             value3 =st.number_input('Steam purchased', key ='value3')
#             value4 =st.number_input('Cooling purchased', key = 'value4')
#             value5 =st.number_input('Electricity, purchased & produced', key = 'value5')
        with col2:
            if st.button('Generate summary statistics for data'):
                values = [value1, value2, value3, value4, value5]
                df = pd.DataFrame(values, columns=["Results"])
                df1 =  df.agg(['sum', 'mean', 'std', 'count','max','min'])
                df2 =df1.round(1)
                st.table(df2)
        if st.checkbox('Visualize'):
            data = {"Fuels, direct accounting": [value1],
            "Fossil fuel heating, estimated": [value2],
            "Steam purchased": [value3],
            "Cooling purchased": [value4],
            "Electricity, purchased & produced": [value5]}
            df = pd.DataFrame(data)
            df_long = df.melt(var_name="Category", value_name="Value")
            df1_long = df_long.sort_values(by =['Value'], ascending = False)
            #st.bar_chart(df1_long, x = 'Category', y='Value')
            fig =alt.Chart(df1_long, title ='Emission by Category').mark_bar().encode(x ='Category', y ='Value', color ='Category')
            st.altair_chart(fig, use_container_width=True, theme ='streamlit')


            
# Example of session state usage.
# st.session_state.value = 50
# value = st.number_input('Enter a number', key='value')
   
# data = {"Fuels, direct accounting": [value1],
#         "Fossil fuel heating, estimated": [value2],
#         "Steam purchased": [value3],
#         "Cooling purchased": [value4],
#         "Electricity, purchased & produced": [value5]}
# df = pd.DataFrame(data)
# df_long = df.melt(var_name="Category", value_name="Value")
# df1_long = df_long.sort_values(by =['Value'], ascending = False)
# #st.bar_chart(df1_long, x = 'Category', y='Value')
# fig =alt.Chart(df1_long, title ='Emission by Category').mark_bar().encode(x ='Category', y ='Value', color ='Category')
# st.altair_chart(fig, use_container_width=True, theme ='streamlit')        
            

    # Build a barchart with altair

                           
            
# elif add_radio == 'Non-Energy':
#     st.subheader('Non energy values')
#     with st.container():
#         col1, col2 = st.columns(2)
#         with col1:
#             value1 =st.number_input('CO2 excluding energy')
#             value2 =st.number_input('Nitrous Oxide')
#             value3 =st.number_input('Methane')
#             value4 =st.number_input('Kyoto Halocarbon')
#             value5 =st.number_input('Non-Kyoto gases')
#             value6 = st.number_input('Agriculture') 
#         with col2:
#             values = [value1, value2, value3, value4, value5, value6]
#             df = pd.DataFrame(values, columns=["Results"])
#             a =  df.agg(['sum', 'mean', 'std', 'count','max','min'])
#             st.table(a)            
       
        
# with st.container():
#     col1, col2 = st.columns(2)
#     with col1:
#         if add_radio == 'Energy':
#             st.subheader('Energy values')
#             value1 =st.number_input('Fuels, direct accounting', step =1)
#             value2 =st.number_input('Fossil fuel heating, estimated', step =1)
#             value3 =st.number_input('Steam purchased', step =1)
#             value4 =st.number_input('Cooling purchased', step =1)
#             value5 =st.number_input('Electricity, purchased & produced', step =1)
#             with col2:
#                  values = [value1, value2, value3, value4, value5]
#                  df = pd.DataFrame(values, columns=["Results"])
#                  a =  df.agg(['sum', 'mean', 'std', 'count','max','min'])
#                  b = a.round(1)
#                  st.dataframe(b)
           
    
     
         
# # NON-ENERGY 2 COMPUTATIONS:
# with st.container():
#     col1, col2 = st.columns(2)
#     with col1:
#         if add_radio == 'Non-Energy':
#             st.subheader('Non-energy values')
#             valuea =st.number_input('CO2 excluding energy', step =1)
#             valueb =st.number_input('Nitrogen Oxyde', step =1)
#             valuec =st.number_input('Methane', step =1)
#             valued =st.number_input('Kyoto holocarbon', step =1)
#             valuee =st.number_input('Non-Kyoto gases', step =1)
#             valuef = st.number_input('Agriculture', step = 1)
#     with col2:
#         values1 = [valuea, valueb, valuec, valued, valuee, valuef]
#         df = pd.DataFrame(values1, columns=["Results"])
#         a =  df.agg(['sum', 'mean', 'std', 'count','max','min'])
#         b = a.round(1)
#         st.dataframe(b)
           
       
            
#https://www.climatiq.io/pricing                
        
           
            
        
        
       
      
             

     

    # Create a DataFrame with the collected values
  

    # Display the DataFrame
  
            
        

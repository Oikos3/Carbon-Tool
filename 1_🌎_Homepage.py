# THis is the landing page or Homepage of the Carbon Tool


# Relevant libraries
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import requests
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from io import BytesIO

# Set page configuration
st.set_page_config(
 page_title = "Homepage",
 layout = 'wide',
page_icon ='🌎',)

#Reduce top space
st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
#Navigation Bar
selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'], 
    icons=['house', 'cloud-upload', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")
selected2

# insert the eolos banner  (Put this in a function and cache it)
@st.cache_data
def read_pic():
    URL = " https://github.com/Brilla1234/My-Datasets/blob/main/eolospane.jpeg?raw=true"
    response = requests.get(URL)
    img = Image.open(BytesIO(response.content))
    new = img.resize((1500,400))
    st.image(new)
read_pic()
     

@st.cache_data
def load_lottieurl(url):
    r =requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()   
#lottie = load_lottieurl("https://assets3.lottiefiles.com/private_files/lf30_ufomdv8u.json")
#st_lottie(lottie, key ='earth', height =100)

# Rule a line
#components.html("""<hr style="height:2.5px;border:none;color:#333;background-color:green;" /> """)
# Create text for the goals, resources data and link of eolos
st.markdown("<h1 style='text-align:center; font-family: Roboto;'> OIKOS 3 </h1>", unsafe_allow_html=True)
st.markdown("### 👨🏼‍💻  The Carbon Writer")
st.markdown("""
Boundless creativity within the planetary boundaries. That is what we stand for! We help you leverage the circular economy principles to 
reduce your CO2 emissions, industrial waste and use of natural resources. That is why we have created this carbon accounting tool
for scope1, 2 and 3 emissions.
Completely automate your GHG accounting process with our robust internal tool!\n 
""")

st.markdown("### 🤖 Resources")
st.markdown(f"""
The program works internally by accessing emission factor data from the Climatiq database using API.
Thanks to [Climatiq API](https://www.climatiq.io/) for providing the resources to pull this data! 
The climatic API enables access to an exhaustive database of emission factors across relevant sectors,
processes, geographies and products.
""")

st.markdown("### 📈 Data")
st.markdown(f"""
The tool is optimized to work with both Excel and CSV files.
Simply upload the file containing the data and experience the magic!👇🏼 \n
You can also input the relevant parameters and generate the estimated Co2 eq
values for the relevant greenhouse gases
""")
st.markdown("### 🔗 Links")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### [🌎 Our Mission](https://www.eolos.org/)")
    # st.image('images/octocat.png', width=150)
    st.write("Read more about our mission to lead companies into a more sustainable future")

with col2:
    st.markdown("### [🗂️ Kaggle](https://www.eolos.org/)")
    # st.image('images/kaggle.png', width=125)
    st.write("Dataset with further details")

with col3:
    st.markdown("### [📺 LinkedIn](https://youtu.be/iNEwkaYmPqY)")
    # st.image('images/youtube.png', width=170)   
    st.write("Follow us on Linkedin")
import streamlit as st
from PIL import Image

st.title("World Temperature Project: Classification Project")

# Write formatted text with bold and normal fonts
st.write("### The Project")
st.markdown(
    """
    &nbsp;&nbsp;&nbsp;&nbsp;The professional formation as Data Analyst hosted by the DataScientest institute will be concluded by this project. It will highlight the knowledge and skills acquired throughout the course of the training,
    which include data cleaning, visualization, the application of a classification model and of course the presentation on a Streamlit page. 
    The contributors are Maria Januszka, Timea Prejbean and David Strüh.
    """,
    unsafe_allow_html=True
)

st.write("<hr>", unsafe_allow_html=True)

#About the project
st.write("### The Objective")
st.markdown(
    """
    &nbsp;&nbsp;&nbsp;&nbsp;Human-made climate change poses a significant threat to humankind and many other species by making the environment uninhabitable for them.  
    The objective of this project is to extend our understanding of it by using the data available to us.
We will try to quantify the extent of global warming and to find the most influential factors. This can be broken down into the following steps:""")
st.write('''•	**Study** historical **trends** in global temperatures  
•	**Gather** additional **data** that might provide an explanation for these developments   
•	**Identify** potential **correlations** using machine learning and rate the impact of the different variables  
•	**Predict** global temperature **changes** in the future
''')
st.write("<hr>", unsafe_allow_html=True)


#Data sources
with st.container():
    st.markdown("### Data Sources")
    sources = [
        "[NASA GISS Surface Temperature Analysis](https://data.giss.nasa.gov/gistemp/)",
        "[Our World in Data, Global Carbon Budget](https://github.com/owid/co2-data/blob/master/owid-co2-codebook.csv)",
        "[Scripps CO² Program](https://scrippsco2.ucsd.edu/data/atmospheric_co2/mlo.html)",
        "[Our World in Data, Population](https://ourworldindata.org/grapher/population?time=1800..latest)",
    ]
    
    st.markdown("The following data sources were used in this project:")
    st.markdown("\n".join([f"- {source}" for source in sources]))

## Add proper citations

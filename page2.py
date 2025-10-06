import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from bokeh.plotting import figure, show, output_notebook
from bokeh.tile_providers import get_provider
from bokeh.models.annotations import BoxAnnotation, Label, Span
from bokeh.palettes import Magma
from bokeh.transform import linear_cmap, transform
from bokeh.layouts import column, row

import plotly.graph_objects as go 
from plotly.subplots import make_subplots


st.title("Data Presentation")

#csv_path = '../data/processed/data.csv'

#uploaded_file = st.file_uploader("Choose a file")

#if uploaded_file is None:
   # st.info("Please upload a file through config")
   # st.stop()
#df = streamlit_data.read_data(uploaded_file)
csv_path_dict = {
    "Global temperature anomalies" : 'GLB_dSST.csv',
    "Temperature anomalies in the northern hemisphere" : 'NH_dSST.csv',
    "Temperature anomalies in the southern hemisphere" : 'SH_dSST.csv',
    "Temperature anomalies by latitude range" : 'ZonAnn.csv',
}   


st.write(
    """
    &nbsp;&nbsp;&nbsp;&nbsp;NASA's Goddard Institute for Space Studies provides us with global temperature data reaching back to 1880. The temperature data consists of
    monthly means that are measured on the earth’s surface both on water and land. However, these are not absolute values. They are the deviations from the mean temperatures
    measured at each measuring point in the reference period from 1951 to 1980. This guarantees the most reliable values and also allows a focus only on temperature change over time.
    """)
st.write(
    """
    The first three provided csv files contain monthly, quarterly and yearly temperature values for the entire planet, the northern and the southern hemisphere respectively. The
    fourth file contains only yearly values but does so for different ranges of latitude. These include the previous three regions, entire planet, northern and southern hemisphere, as well as
    partitions of 3 and 8.
    """)

st.markdown("<hr>", unsafe_allow_html=True)



option = st.selectbox('Choice of the CSV file to be loaded', ["Select"] + list(csv_path_dict.keys()))

if option != "Select":
    col1,col2,col3,col4 = st.columns([1,1,1,1])
    selected_path = csv_path_dict[option]
    df = pd.read_csv(selected_path)
    with col1:
        if st.toggle('Clean'):
            df = df.replace('***', np.NaN)
            df = df.astype('float')
            if option != 'Temperature anomalies by latitude range':
                df.loc[0,'D-N'] = df.iloc[0,1:11].mean()
                df.loc[0,'DJF'] = df.iloc[0,1:2].mean()
                df_q_tempchange = []
                df_q_date = []
                df_q_tag = []
                for index, row in df.iterrows():
                    df_q_tempchange.extend((row['DJF'], row['MAM'],row['JJA'],row['SON']))
                    df_q_tag.extend(('DJF','MAM','JJA','SON'))
                    df_q_date.extend((datetime.datetime(index+1880,1,1), datetime.datetime(index+1880,4,1),datetime.datetime(index+1880,7,7),datetime.datetime(index+1880,10,1)))
                df_m_tempchange = []
                df_m_date = []
                df_m_tag = []
                for index, row in df.iterrows():
                    df_m_tempchange.extend((row['Jan'],row['Feb'],row['Mar'],row['Apr'],row['May'],row['Jun'],row['Jul'],row['Aug'],row['Sep'],row['Oct'],row['Nov'],row['Dec']))
                    df_m_date.extend((datetime.datetime(index+1880,1,1), datetime.datetime(index+1880,2,1), datetime.datetime(index+1880,3,1), datetime.datetime(index+1880,4,1),
                                      datetime.datetime(index+1880,5,1), datetime.datetime(index+1880,6,1), datetime.datetime(index+1880,7,1), datetime.datetime(index+1880,8,1),
                                      datetime.datetime(index+1880,9,1), datetime.datetime(index+1880,10,1), datetime.datetime(index+1880,11,1), datetime.datetime(index+1880,12,1),))
                dict_q = {'Temp_Change': df_q_tempchange, 'Date': df_q_date, 'tag': df_q_tag}
                df_q = pd.DataFrame(dict_q)
                dict_m = {'Temp_Change': df_m_tempchange, 'Date': df_m_date}
                df_m = pd.DataFrame(dict_m)
                
        
    choice = csv_path_dict.keys
        #st.write('The chosen CSV is :', option)
        # Step 1: Button to Proceed
    
    with st.expander(f'Preview of {option}', expanded=True):
        st.dataframe(df,column_config={'Year':st.column_config.NumberColumn(format='%d')})

    if option != 'Temperature anomalies by latitude range':
        df['Date'] = pd.to_datetime(df.Year, format='%Y')


st.markdown(
    """
    #### Data cleaning:
    • The three dataframes with monthly values required some cleaning, because they contain placeholders where there is not sufficient data available. This does, however, only occur in the first and the last row of the dataframe.  
    •	In the first row, which represents the first your of temperature measurements, the two columns ‘D-N’ and ‘DJF’ include a month which is outside of the relevant timeframe. The values are replaced with the averages excluding December 1879.  
    •	The last row, which shows the data for the current year, shows placeholders where there is no data available yet. These placeholders are replaced with NaN values.  
    •	In the next step, all values can be converted to two-digit floats.  
    •	The fourth dataframe did not require any cleaning at all.  
    """
    )

st.markdown("<hr>", unsafe_allow_html=True)

if option != 'Select':
    st.title("Visualization of temperature data")

    if option != 'Temperature anomalies by latitude range':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.Date,y=df['J-D'], name='J-D', legendgroup='Yearly', legendgrouptitle={'text':'Yearly'}))
        fig.add_trace(go.Scatter(x=df.Date,y=df['D-N'], name='D-N', legendgroup='Yearly', legendgrouptitle={'text':'Yearly'}))
        fig.add_trace(go.Scatter(x=df_q.Date, y= df_q.Temp_Change, name = 'Quarterly'))
        fig.add_trace(go.Scatter(x=df_m.Date, y= df_m.Temp_Change, name = 'Monthly'))
        fig.update_layout(legend_groupclick='toggleitem')

        st.plotly_chart(fig)

if option =='Temperature anomalies by latitude range':
    zone = df
    zone = zone.set_index('Year')

    fig = make_subplots(rows=2,cols=2, subplot_titles=('Global', '2 zones', '3 zones', '8 zones'), vertical_spacing=0.07, horizontal_spacing=0.02) 

    fig.add_trace(go.Scatter(y=zone['Glob'], x=zone.index, text='Global', name='Global', legendgroup='Global'), row=1,col=1)
    fig.add_trace(go.Scatter(y=zone['NHem'], x=zone.index, text='North', name='North', legendgroup='2 zones', legendgrouptitle={'text': '2 zones'}),row=1,col=2)
    fig.add_trace(go.Scatter(y=zone['SHem'], x=zone.index, text='South', name='South', legendgroup='2 zones', legendgrouptitle={'text': '2 zones'}),row=1,col=2)
    fig.add_trace(go.Scatter(y=zone['24N-90N'], x=zone.index, text='24N-90N', name='24N-90N', legendgroup='3 zones', legendgrouptitle={'text': '3 zones'}),row=2,col=1)
    fig.add_trace(go.Scatter(y=zone['24S-24N'], x=zone.index, text='24S-24N', name='24S-24N', legendgroup='3 zones', legendgrouptitle={'text': '3 zones'}),row=2,col=1)
    fig.add_trace(go.Scatter(y=zone['90S-24S'], x=zone.index, text='90S-24S', name='90S-24S', legendgroup='3 zones', legendgrouptitle={'text': '3 zones'}),row=2,col=1)
    fig.add_trace(go.Scatter(y=zone['64N-90N'], x=zone.index, text='64N-90N', name='64N-90N', legendgroup='8 zones', legendgrouptitle={'text': '8 zones'}),row=2,col=2)
    fig.add_trace(go.Scatter(y=zone['44N-64N'], x=zone.index, text='44N-64N', name='44N-64N', legendgroup='8 zones', legendgrouptitle={'text': '8 zones'}),row=2,col=2)
    fig.add_trace(go.Scatter(y=zone['24N-44N'], x=zone.index, text='24N-44N', name='24N-44N', legendgroup='8 zones', legendgrouptitle={'text': '8 zones'}),row=2,col=2)
    fig.add_trace(go.Scatter(y=zone['EQU-24N'], x=zone.index, text='EQU-24N', name='EQU-24N', legendgroup='8 zones', legendgrouptitle={'text': '8 zones'}),row=2,col=2)
    fig.add_trace(go.Scatter(y=zone['24S-EQU'], x=zone.index, text='24S-EQU', name='24S-EQU', legendgroup='8 zones', legendgrouptitle={'text': '8 zones'}),row=2,col=2)
    fig.add_trace(go.Scatter(y=zone['44S-24S'], x=zone.index, text='44S-24S', name='44S-24S', legendgroup='8 zones', legendgrouptitle={'text': '8 zones'}),row=2,col=2)
    fig.add_trace(go.Scatter(y=zone['64S-44S'], x=zone.index, text='64S-44S', name='64S-44S', legendgroup='8 zones', legendgrouptitle={'text': '8 zones'}),row=2,col=2)
    fig.add_trace(go.Scatter(y=zone['90S-64S'], x=zone.index, text='90S-64S', name='90S-64S', legendgroup='8 zones', legendgrouptitle={'text': '8 zones'}),row=2,col=2)

    fig.update_layout(height=700, yaxis_range=[-2.5,3.2], yaxis2_range=[-2.5,3.2], yaxis3_range=[-2.5,3.2], yaxis4_range=[-2.5,3.2])
    fig.update_layout(yaxis2={'showticklabels':False},yaxis4={'showticklabels':False},
                    xaxis1={'showticklabels':False},xaxis2={'showticklabels':False})
    fig.update_layout(legend_groupclick='toggleitem')

    st.plotly_chart(fig)

#Check if the other DataFrames were loaded correctly for the next pages
not_loaded = []
for key in ['df_Zon']:
    df = getattr(st.session_state, key)
    if df is None:
        not_loaded.append(key)
    elif isinstance(df, pd.DataFrame) and df.empty:
        not_loaded.append(key)

# Display the result
if not_loaded:
    st.error(f"The following DataFrames were not loaded correctly: {', '.join(not_loaded)}")
else:
    st.success("All DataFrames were loaded successfully!")

import streamlit as st
import matplotlib.pyplot as plt
import streamlit_data
import streamlit_widgets
import pandas as pd
import numpy as np
import datetime
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import LinearColorMapper, ColorBar, ColumnDataSource, CustomJS, Slider, Range1d, LinearAxis, Tabs, Panel
from bokeh.tile_providers import get_provider, Vendors
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

    ## Definition of the color scheme

    cmap = plt.colormaps['seismic']

    ## Definition of the outer values

    colormap_min = -3.5                       #zone.min().min() 
    colormap_max = 3.5                        #zone.max().max() 
    colormap_range = colormap_max - colormap_min

    ## Definition of the opacity

    fill_alpha = 0.5

    def get_color(colname):
        box_colname_color_code = ((zone[colname].loc[zone.index == yearvalue]-colormap_min)/colormap_range).iloc[0]
        box_colname_color = []
        for i in range(3): box_colname_color.append(cmap(box_colname_color_code, bytes=True)[i])
        return box_colname_color

    def get_temp(colname):
        temp_colname = "{0:+.02f}".format(zone[colname].loc[zone.index == yearvalue].iloc[0])+'°C'
        return temp_colname

    def go_temp(temp_diff):
        temp_str = "{0:+.02f}".format(temp_diff)+'°C'
        return temp_str

    def rgb_color(temp_diff):
        temp_color_code = (temp_diff-colormap_min)/colormap_range
        temp_color = []
        for i in range(3): temp_color.append(cmap(temp_color_code, bytes=True)[i])
        return temp_color

    def rgba_color(temp_diff):
        temp_color_code = (temp_diff-colormap_min)/colormap_range
        temp_color = []
        for i in range(3): temp_color.append(cmap(temp_color_code, bytes=True)[i])
        return 'rgba('+str(temp_color[0])+','+str(temp_color[1])+','+str(temp_color[2])+','+str(fill_alpha)+')'

    # Function to get the correct y coordinate for the degrees latitude of the mercator projection

    def latitude(degree):
        k = 6378137
        return np.log(np.tan((90 + degree) * np.pi/360.0)) * k




    data = pd.DataFrame(columns=['Group','Region', 'Year','Temp_Value','Temp_Str'])
    df = pd.DataFrame()
    for i in zone.columns:
        df['Temp_Value'] = zone[i] 
        df['Temp_Str'] = zone[i].apply(go_temp)
        df['Region'] = i
        df['Year'] = zone.index
        data = pd.concat([data, df], ignore_index=True, axis=0)

    reg_dict = {'Glob':'Entire Planet', 'NHem':'2 Zones', 'SHem':'2 Zones', '24N-90N':'3 Zones', '24S-24N':'3 Zones', '90S-24S':'3 Zones',
                                    '64N-90N':'8 Zones', '44N-64N':'8 Zones', '24N-44N':'8 Zones', 'EQU-24N':'8 Zones', '24S-EQU':'8 Zones',
                                    '44S-24S':'8 Zones', '64S-44S':'8 Zones', '90S-64S':'8 Zones'}

    data['Group'] =  data.Region.map(reg_dict)
    data['RGB'] = data.Temp_Value.apply(rgb_color)
    data['RGBA'] = data.Temp_Value.apply(rgba_color)

    Lat_North = []
    for i in [90,90,0,90,24,-24,90,64,44,24,0,-24,-44,-64]:
        for j in range(len(df)):
            Lat_North.append(i)

    data['Lat_North'] = Lat_North

    Lat_South = []
    for i in [-90,0,-90,24,-24,-90,64,44,24,0,-24,-44,-64,-90]:
        for j in range(len(df)):
            Lat_South.append(i)

    data['Lat_South'] = Lat_South
    data['Lat_Text'] = (data.Lat_North+data.Lat_South)/2
    data['Lon_Text'] = 0

    ## Now we create lists of coordinates for the mapboxes and add them to the dataframe, first latitude and longitude separately and then together.
    ## We'll see later which one we'll need

    mblatlist = []
    for i,j  in zip(data['Lat_North'],data['Lat_South']):
        k = [i,i,j,j,i]
        mblatlist.append(k)
    data['MB_Lat'] = mblatlist

    mblonlist = []
    for i in range(len(data.index)):
        mblonlist.append([180,-180,-180,180,180])
    data['MB_Lon'] = mblonlist

    mbcoolist = []
    for i,j  in zip(data['Lat_North'],data['Lat_South']):
        k = [[180,i],[-180,i],[-180,j],[180,j],[180,i]]
        mbcoolist.append(k)
    data['MB_Coord'] = mbcoolist



    #range bounds supplied in web mercator coordinates
    p1 = figure(x_range=(-18000000, 18000000), y_range=(-18000000, 18000000), y_axis_type="mercator", x_axis_type='mercator')
    p2 = figure(x_range=(-18000000, 18000000), y_range=(-18000000, 18000000), y_axis_type="mercator", x_axis_type='mercator')
    p3 = figure(x_range=(-18000000, 18000000), y_range=(-18000000, 18000000), y_axis_type="mercator", x_axis_type='mercator')
    p4 = figure(x_range=(-18000000, 18000000), y_range=(-18000000, 18000000), y_axis_type="mercator", x_axis_type='mercator')

    # World map

    tile_a = get_provider('CARTODBPOSITRON')
    tile_b = get_provider('CARTODBPOSITRON')
    tile_c = get_provider('CARTODBPOSITRON')
    tile_d = get_provider('CARTODBPOSITRON')

    yearvalue = st.slider('year',min_value=1880, max_value=2024, value=None, step=1)

    ## Boxes

    # The entire planet

    box_g = BoxAnnotation(top=latitude(90),  bottom=-20000000,     fill_color=get_color('Glob'),    fill_alpha=fill_alpha)

    # Northern hemisphere vs southern hemisphere
    # NHem Shem

    box_n = BoxAnnotation(top=latitude(90),  bottom=0,             fill_color=get_color('NHem'),    fill_alpha=fill_alpha)
    box_s = BoxAnnotation(top=0,             bottom=-20000000,     fill_color=get_color('SHem'),    fill_alpha=fill_alpha)

    # North vs tropics vs south
    # 24N-90N 	24S-24N 	90S-24S

    box_a = BoxAnnotation(top=latitude(90),  bottom=latitude(24),  fill_color=get_color('24N-90N'), fill_alpha=fill_alpha)
    box_b = BoxAnnotation(top=latitude(24),  bottom=latitude(-24), fill_color=get_color('24S-24N'), fill_alpha=fill_alpha)
    box_c = BoxAnnotation(top=latitude(-24), bottom=-20000000,     fill_color=get_color('90S-24S'), fill_alpha=fill_alpha)

    # 8 steps from north to south
    # 64N-90N 	44N-64N 	24N-44N 	EQU-24N 	24S-EQU 	44S-24S 	64S-44S 	90S-64S

    box_1 = BoxAnnotation(top=latitude(90),  bottom=latitude(64),  fill_color=get_color('64N-90N'), fill_alpha=fill_alpha)
    box_2 = BoxAnnotation(top=latitude(64),  bottom=latitude(44),  fill_color=get_color('44N-64N'), fill_alpha=fill_alpha)
    box_3 = BoxAnnotation(top=latitude(44),  bottom=latitude(24),  fill_color=get_color('24N-44N'), fill_alpha=fill_alpha)
    box_4 = BoxAnnotation(top=latitude(24),  bottom=0,             fill_color=get_color('EQU-24N'), fill_alpha=fill_alpha)
    box_5 = BoxAnnotation(top=0,             bottom=latitude(-24), fill_color=get_color('24S-EQU'), fill_alpha=fill_alpha)
    box_6 = BoxAnnotation(top=latitude(-24), bottom=latitude(-44), fill_color=get_color('44S-24S'), fill_alpha=fill_alpha)
    box_7 = BoxAnnotation(top=latitude(-44), bottom=latitude(-64), fill_color=get_color('64S-44S'), fill_alpha=fill_alpha)
    box_8 = BoxAnnotation(top=latitude(-64), bottom=-20000000,     fill_color=get_color('90S-64S'), fill_alpha=fill_alpha)

    ## Temperature labels

    lab_g = Label(x=0,y=0,            text=get_temp('Glob'),    x_offset=-25, y_offset=-10)      # entire planet

    lab_n = Label(x=0,y=latitude(45), text=get_temp('NHem'),    x_offset=-25, y_offset=-10)      # north vs south
    lab_s = Label(x=0,y=latitude(-45),text=get_temp('SHem'),    x_offset=-25, y_offset=-10)

    lab_a = Label(x=0,y=latitude(57), text=get_temp('24N-90N'), x_offset=-25, y_offset=-10)      # north vs tropics vs south
    lab_b = Label(x=0,y=0,            text=get_temp('24S-24N'), x_offset=-25, y_offset=-10)
    lab_c = Label(x=0,y=latitude(-57),text=get_temp('90S-24S'), x_offset=-25, y_offset=-10)

    lab_1 = Label(x=0,y=latitude(77), text=get_temp('64N-90N'), x_offset=-25, y_offset=-10)      # 8 steps from north to south
    lab_2 = Label(x=0,y=latitude(55), text=get_temp('44N-64N'), x_offset=-25, y_offset=-10)
    lab_3 = Label(x=0,y=latitude(34), text=get_temp('24N-44N'), x_offset=-25, y_offset=-10)
    lab_4 = Label(x=0,y=latitude(12), text=get_temp('EQU-24N'), x_offset=-25, y_offset=-10)
    lab_5 = Label(x=0,y=latitude(-12),text=get_temp('24S-EQU'), x_offset=-25, y_offset=-10)
    lab_6 = Label(x=0,y=latitude(-34),text=get_temp('44S-24S'), x_offset=-25, y_offset=-10)
    lab_7 = Label(x=0,y=latitude(-55),text=get_temp('64S-44S'), x_offset=-25, y_offset=-10)
    lab_8 = Label(x=0,y=latitude(-77),text=get_temp('90S-64S'), x_offset=-25, y_offset=-10)


    ## Layouts

    p1.add_layout(box_g)     # entire planet
    p1.add_layout(lab_g)
    p1.add_tile(tile_a)


    p2.add_layout(box_n)     # north vs south 
    p2.add_layout(box_s)
    p2.add_layout(lab_n)      
    p2.add_layout(lab_s)
    p2.add_tile(tile_b)


    p3.add_layout(box_a)        # north vs tropics vs south
    p3.add_layout(box_b)
    p3.add_layout(box_c)  
    p3.add_layout(lab_a)        
    p3.add_layout(lab_b)
    p3.add_layout(lab_c)
    p3.add_tile(tile_c)


    p4.add_layout(box_1)        # 8 steps from north to south
    p4.add_layout(box_2)
    p4.add_layout(box_3)
    p4.add_layout(box_4)
    p4.add_layout(box_5)
    p4.add_layout(box_6)
    p4.add_layout(box_7)
    p4.add_layout(box_8)
    p4.add_layout(lab_1)      
    p4.add_layout(lab_2)
    p4.add_layout(lab_3)
    p4.add_layout(lab_4)
    p4.add_layout(lab_5)
    p4.add_layout(lab_6)
    p4.add_layout(lab_7)
    p4.add_layout(lab_8)
    p4.add_tile(tile_d)

    tab1 = Panel(child=p1, title='global')
    tab2 = Panel(child=p2, title='2 zones')
    tab3 = Panel(child=p3, title='3 zones')
    tab4 = Panel(child=p4, title='8 zones')

    tabs = Tabs(tabs=[tab1,tab2,tab3,tab4])


    st.bokeh_chart(tabs)


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

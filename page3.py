import plotly.graph_objects as go 
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.title("Additional data")

st.markdown(
    """
    What is causing this increase in surface temperature? Scientists agree that CO2 is the primary driver of humanmade climate change. So let's have a look at the global CO2 emissions.
    Additionally, we will include other greenhouse gases like Nitrous Oxide and methane in our examinations.
    Then again, the greenhouse effect relies on the gases that have accumulated in the atmosphere rather than just those that are being added every year. So the atmospheric CO2 will be added to our data.


    Another interesting statistic to look at would be the number of human beings living on this planet. 
    """,
    unsafe_allow_html=True
)


csv_path_dict = {
    "Global greenhouse gas emissions" : 'owid-co2-data.csv',
    "Population": 'population.csv',
    "Atmospheric CO2": 'monthly_in_situ_co2_mlo.csv'
}

relcols = ['country','year','population','co2','co2_including_luc','nitrous_oxide','methane']
makeplot = False

# Initialize session state for DataFrames
if "df_CO2" not in st.session_state:
    st.session_state.df_CO2 = pd.DataFrame()
if "df_Atm" not in st.session_state:
    st.session_state.df_Atm = pd.DataFrame()

choice = csv_path_dict.keys
option = st.selectbox('Choice of the CSV file to be loaded', ["Select"] + list(csv_path_dict.keys()))



## option2 = st.selectbox('Choice of columns to include', ['Select'] + streamlit_data.read_data(csv_path_dict[option]).columns.tolist())

#st.write('The chosen CSV is :', option)
    # Step 1: Button to Proceed
if option == "Global greenhouse gas emissions":
    selected_path = csv_path_dict[option]
    col1,col2,col3 = st.columns([1,1,1])
    df_ghg = pd.read_csv(selected_path)
    with col1:
        if st.toggle('Filter by World'):
            df_ghg = df_ghg.loc[df_ghg.country == 'World']
            df_ghg = df_ghg.drop(['iso_code'],axis=1)
            makeplot = True
    with col2:
        if st.toggle('Filter by years'):
            df_ghg = df_ghg.loc[df_ghg.year > 1879]
    with col3:
        if st.toggle('Filter relevant columns'):
            df_ghg = df_ghg[relcols]
    with st.expander(f'Preview of {option}', expanded=True):
        st.dataframe(df_ghg,column_config={'year':st.column_config.NumberColumn(format='%d')})
if option == 'Population':
    selected_path = csv_path_dict[option]
    col1,col2,col3 = st.columns([1,1,1])
    df_pop = streamlit_data.read_data(selected_path)
    df_pop = df_pop.drop(['Code'],axis=1)
    with col1:
        if st.toggle('Filter by World'):
            df_pop = df_pop[df_pop.Entity == 'World']
    with col2:
        if st.toggle('Filter by years'):
            df_pop = df_pop[df_pop.Year > 1879]
    with st.expander(f'Preview of {option}', expanded=True):
        st.dataframe(df_pop,column_config={'Year':st.column_config.NumberColumn(format='%d')})        
if option == "Atmospheric CO2":
    selected_path = csv_path_dict[option]
    col1,col2,col3,col4 = st.columns([1,1,1,1])
    df_atm = streamlit_data.read_data(selected_path)
    df_atm = df_atm.rename(columns={'Yr':'Year'})
    xticks = [24,264,504,744]
    xtext = [1960,1980,2000,2020]
    with col2:
        if st.toggle('Clean'):
            df_atm = df_atm.replace(-99.99, np.NaN)
            df_atm = df_atm.fillna(method='ffill')
            df_atm = df_atm.fillna(method='bfill')
    with col1:
        if st.toggle('Drop columns'):
            df_atm = df_atm.drop(['Date','Date.1','Sta'], axis=1)
            df_atm = df_atm.drop(['Mn'], axis=1)
            with col3:
                if st.toggle('Yearly means'):
                    df_atm = df_atm.groupby(df_atm['Year']).mean()
                    df_atm = df_atm.reset_index()
                    xticks = [2,22,42,62]                    
                    with col4:
                        if st.toggle('CO2-Model'):
                            est_ppm = streamlit_data.read_data('D:/sachen/jobs/data analysis/world temp project/est_ppm.csv')
                            df_atm = pd.merge(df_atm,est_ppm, on='Year', how='outer')
                            df_atm = df_atm.sort_values('Year')
                            df_atm = df_atm.drop('Unnamed: 0', axis=1)
                            df_atm = df_atm[df_atm['Year'] > 1879]
                            df_atm = df_atm.reset_index()
                            df_atm = df_atm.drop(['index'], axis=1)
                            xticks = [0,20,40,60,80,100,120,140]
                            xtext = [1880,1900,1920,1940,1960,1980,2000,2020]



    with st.expander(f'Preview of {option}', expanded=True):
        st.dataframe(df_atm,column_config={'Year':st.column_config.NumberColumn(format='%d')})


st.markdown("<hr>", unsafe_allow_html=True)

if option != "Select":
    st.title("Visualization of the data")
if option == "Global greenhouse gas emissions" and makeplot == True:
    fig = make_subplots(specs=[[{'secondary_y':True}]])
    fig.add_trace(go.Scatter(x = df_ghg['year'], y = df_ghg.population, text ='Population', name ='Population'))
    for col in df_ghg.columns[3:]:
        fig.add_trace(go.Scatter(x= df_ghg.year, y = df_ghg[col], name=col), secondary_y=True)
    
                  
    fig.update_layout(height=700)
    fig.update_yaxes(title_text='Gt (CO2 equivalent)', secondary_y=True)
    fig.update_yaxes(title_text='People', secondary_y=False)

    st.plotly_chart(fig)
if option == "Population":
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_pop.Year, y=df_pop['Population (historical)'], name = "Population"))
    st.plotly_chart(fig)
if option == "Atmospheric CO2":
    fig = go.Figure()
    for col in df_atm.columns[1:]:
        fig.add_trace(go.Scatter(x= df_atm.index, y = df_atm[col], name=col))
    fig.update_yaxes(title_text='ppm')
    fig.update_xaxes(tickmode = 'array',
                     tickvals = xticks,
                     ticktext = xtext)


    st.plotly_chart(fig)
                    
'''
    if option == 'Global greenhouse gas emissions' in option:
        if st.session_state.df_CO2.empty:
            st.session_state.df_CO2 = df
    elif option == 'Atmospheric CO2' in option:
        if st.session_state.df_Atm.empty:
            st.session_state.df_SH = df
    

        '''

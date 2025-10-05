import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression


st.title("Machine Learning")


st.markdown(
    """
    &nbsp;&nbsp;&nbsp;&nbsp;Lorem ipsum

    """
)

df = pd.read_csv('data.csv')
df = df.set_index('Year')
df_fin = df.drop(['CO2_ex','ppm','Population','N2O','CH4','CO2_in'], axis=1)

col1,col2,col3,col4,col5, col6 = st.columns(6)

with col1:
    if st.toggle('CO2_ex', value=True):
        df_fin['CO2_ex'] = df['CO2_ex']
with col2:
    if st.toggle('CO2_in', value=True):
        df_fin['CO2_in'] = df['CO2_in']
with col3:
    if st.toggle('ppm', value=True):
        df_fin['ppm'] = df['ppm']
with col4:
    if st.toggle('Population', value=True):
        df_fin['Population'] = df['Population']
with col5:
    if st.toggle('N2O', value=True):
        df_fin['N2O'] = df['N2O']
with col6:
    if st.toggle('CH4', value=True):
        df_fin['CH4'] = df['CH4']

rfr = RandomForestRegressor(max_depth=1, random_state=121)
dtr = DecisionTreeRegressor(max_depth=1, random_state=121)
lre = LinearRegression()
algorithms = {'Random Forest Regressor' : rfr, 'Decision Tree Regressor' : dtr, 'Linear Regression' : lre}


with st.expander(f'Preview of final dataframe', expanded=True):
    st.dataframe(df_fin,column_config={'Year':st.column_config.NumberColumn(format='%d')})

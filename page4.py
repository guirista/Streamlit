import streamlit as st
import numpy as np
import streamlit_data
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

csv_path_dict = 'data.csv'

df = streamlit_data.read_data(csv_path_dict)


with st.expander(f'Preview of final dataframe', expanded=True):
    st.dataframe(df,column_config={'Year':st.column_config.NumberColumn(format='%d')})

import streamlit as st
import numpy as np
import pandas as pd


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

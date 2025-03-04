import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('train.csv')

st.title("Titanic : binary classification project")
st.sidebar.title("Table of contents")
pages=["Exploration", "DataVizualization", "Modelling"]
page=st.sidebar.radio("Go to", pages)

if page == pages[0] :
    st.write('### Presentation of data')
    st.dataframe(df.head(10))
    st.write(df.shape)
    st.dataframe(df.describe())

    if st.checkbox('Show NA') :
        st.dataframe(df.isna().sum())


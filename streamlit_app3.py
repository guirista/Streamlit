import streamlit as st
import pandas as pd
import seaborn as sns
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

if page == pages[1] : 
    st.write('### DataVizualization')
    fig = plt.figure()
    sns.countplot(x = 'Survived', data =df)
    st.pyplot(fig)

    fig = plt.figure()
    sns.countplot(x = 'Sex', data=df)
    plt.title('Distribution of passengers gender')
    st.pyplot(fig)

    fig = plt.figure()
    sns.countplot(x='Pclass',data=df)
    plt.title('Distribution of passengers class')
    st.pyplot(fig)
    
    fig=plt.figure()
    sns.countplot(x='Age',data=df)
    plt.title('Distribution of the passengers age')
    st.pyplot(fig)

    fig=plt.figure()
    sns.countplot(x='Survived',hue='Sex',data=df)
    st.pyplot(fig)

    fig= sns.catplot(x='Pclass', y='Survived', data=df, kind='point')
    st.pyplot(fig)

    fig = sns.lmplot(x='Age', y='Survived', hue='Pclass', data=df)
    st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.heatmap(df.select_dtypes(['number']).corr(), ax=ax)
    st.write(fig)

    st.write('### Modelling')

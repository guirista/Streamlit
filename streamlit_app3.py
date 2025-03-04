import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn

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

if page == pages[2] :
    st.write('### Modelling')

    df = df.drop(['PassengerId','Name','Ticket','Cabin'], axis=1)

    y= df['Survived']
    X_cat  =df[['Pclass','Sex','Embarked']]
    X_num = df[['Age','Fare','SibSp','Parch']]
    
    for col in X_cat.columns:
        X_cat[col] = X_cat[col].fillna(X_cat[col].mode()[0])
    for col in X_num.columns:
        X_num[col] = X_num[col].fillna(X_num[col].median())
    X_cat_scaled = pd.get_dummies(X_cat, columns=X_cat.columns)
    X = pd.concat([X_cat_scaled, X_num], axis=1)
    
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=123)

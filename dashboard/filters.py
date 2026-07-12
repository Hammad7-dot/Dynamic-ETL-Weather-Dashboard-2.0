import streamlit as st


def filter_data(df):

    cities = sorted(df["city"].dropna().unique())

    city = st.sidebar.selectbox("City", ["All"] + cities)

    if city != "All":
        df = df[df["city"] == city]

    return df

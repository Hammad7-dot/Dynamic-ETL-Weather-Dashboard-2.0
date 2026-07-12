import plotly.express as px
import streamlit as st


def temperature_chart(df):
    multi_city = df["city"].nunique() > 1

    fig = px.line(
        df.sort_values("timestamp"),
        x="timestamp",
        y="temperature",
        color="city" if multi_city else None,
        markers=True,
        title="Temperature Trend",
    )

    st.plotly_chart(fig, use_container_width=True)


def humidity_chart(df):
    multi_city = df["city"].nunique() > 1

    fig = px.bar(
        df.sort_values("timestamp"),
        x="timestamp",
        y="humidity",
        color="city" if multi_city else None,
        barmode="group" if multi_city else "relative",
        title="Humidity",
    )

    st.plotly_chart(fig, use_container_width=True)


def weather_distribution(df):
    fig = px.pie(df, names="weather", title="Weather Distribution")

    st.plotly_chart(fig, use_container_width=True)

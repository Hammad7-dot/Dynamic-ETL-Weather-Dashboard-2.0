import streamlit as st


def export_csv(df):

    csv = df.to_csv(index=False)

    st.download_button("⬇ Download CSV", csv, "weather.csv", "text/csv")

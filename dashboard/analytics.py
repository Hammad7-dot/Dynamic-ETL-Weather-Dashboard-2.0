import plotly.express as px
import streamlit as st


def analytics(df):

    st.subheader("📈 Weather Analytics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Average Temperature", f"{df['temperature'].mean():.1f} °C")
    col2.metric("Maximum Temperature", f"{df['temperature'].max():.1f} °C")
    col3.metric("Minimum Temperature", f"{df['temperature'].min():.1f} °C")

    st.markdown("---")

    col4, col5 = st.columns(2)

    col4.metric("Average Humidity", f"{df['humidity'].mean():.0f}%")
    col5.metric("Average Wind Speed", f"{df['wind_speed'].mean():.1f} m/s")

    st.markdown("---")
    _day_hour_patterns(df)


def _day_hour_patterns(df):
    """Average temperature by day-of-week and by hour, when we have enough
    history for the patterns to mean something."""
    if df["timestamp"].dt.date.nunique() < 2 and df.shape[0] < 8:
        st.caption("Collect a bit more history for day/hour pattern charts to show up here.")
        return

    st.markdown("##### Patterns over time")
    c1, c2 = st.columns(2)

    with c1:
        by_day = (
            df.groupby("day", as_index=False)["temperature"]
            .mean()
            .reindex()
        )
        order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        by_day["day"] = by_day["day"].astype(str)
        by_day = by_day.set_index("day").reindex(order).dropna().reset_index()
        fig = px.bar(by_day, x="day", y="temperature", title="Avg temperature by day of week")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        by_hour = df.groupby("hour", as_index=False)["temperature"].mean().sort_values("hour")
        fig = px.line(by_hour, x="hour", y="temperature", markers=True, title="Avg temperature by hour")
        st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Trend ocen aplikacji", layout="wide")
st.title("Trend ocen aplikacji mobilnych w czasie")

@st.cache_data
def load_data():
    return pd.read_csv("mobilerec_data.csv", parse_dates=["formated_date"])

df = load_data()

mode = st.radio("Wybierz tryb analizy:", ["Pojedyncza aplikacja", "Kategoria aplikacji"])

if mode == "Pojedyncza aplikacja":
    selected_app = st.selectbox("Wybierz aplikację (package):", df["app_package"].unique())
    df_filtered = df[df["app_package"] == selected_app]

    trend = df_filtered.groupby("formated_date")["rating"].mean().reset_index()

    fig = px.line(
        trend,
        x="formated_date",
        y="rating",
        title=f"Średnia ocena aplikacji: {selected_app}",
        labels={"formated_date": "Data", "rating": "Średnia ocena"}
    )
    st.plotly_chart(fig, use_container_width=True)

elif mode == "Kategoria aplikacji":
    selected_cat = st.selectbox("Wybierz kategorię:", df["app_category"].dropna().unique())
    df_filtered = df[df["app_category"] == selected_cat]

    trend = df_filtered.groupby("formated_date")["rating"].mean().reset_index()

    fig = px.line(
        trend,
        x="formated_date",
        y="rating",
        title=f"Średnia ocena w kategorii: {selected_cat}",
        labels={"formated_date": "Data", "rating": "Średnia ocena"}
    )
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Pokaż dane źródłowe"):
    st.dataframe(df_filtered.sort_values("formated_date"))

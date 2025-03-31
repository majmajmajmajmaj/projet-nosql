import streamlit as st
from src.mongodb import getGetYearWithMostMovies

st.title("Projet MongoDB - Analyse de films")
st.subheader("Année avec le plus de films sorties :")

yearInfo = getGetYearWithMostMovies()

if yearInfo:
    st.write(f"**{yearInfo['_id']}** avec **{yearInfo['count']}** films.")
else:
    st.write("Pas trouv")
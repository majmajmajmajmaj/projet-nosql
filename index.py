import streamlit as st
from src.mongodb import getGetYearWithMostMovies, countMoviesAfter1999, averageVotes2007, getMoviesCountPerYear, getAllGenres, getHighestRevenueMovie, getDirectorsWithMoreThan5Movies
import matplotlib.pyplot as plt

st.title("Projet MongoDB - Analyse de films")

#Question 1
st.subheader("1. Afficher l’année où le plus grand nombre de films ont été sortis.")

yearInfo = getGetYearWithMostMovies()

st.write(f"**{yearInfo['_id']}** avec **{yearInfo['count']}** films.")
st.write("Pas trouv")


# Question 2
count = countMoviesAfter1999()
st.subheader("2. Quel est le nombre de films sortis après l’année 1999.")
st.write(f"Il y a **{count}** films sorties après 1999.")


#Question 3
votes = averageVotes2007()
st.subheader("3. Quelle est la moyenne des votes des films sortis en 2007.")
st.write(f"la moyenne des votes est **{votes}**.")


#Question4
st.subheader("4. Affichez un histogramme qui permet de visualiser le nombres de films par année.")
data = getMoviesCountPerYear()

anneee = [item['_id'] for item in data if item['_id'] is not None]
counts = [item['count'] for item in data if item['_id'] is not None]

plt.figure(figsize=(10, 4))
plt.bar(anneee, counts)
plt.xlabel("Année")
plt.ylabel("Nombre de films")
plt.title("Nombre de films par année")
st.pyplot(plt)

#Question 5
st.subheader("5. Quelles sont les genres de films disponibles dans la bases")

genres = getAllGenres()

st.write(f"Il y a **{len(genres)}** genres .")
st.write(", ".join(genres))


# Question 6
st.subheader("6. Quel est le film qui a généré le plus de revenu.")

movie = getHighestRevenueMovie()
st.write(f"**{movie['title']}** a généré **{movie['Revenue (Millions)']} millions**.")

# Question 7
st.subheader("7. Quels sont les réalisateurs ayant réalisé plus de 5 films dans la base de données ?")

directors = getDirectorsWithMoreThan5Movies()
if directors:
    for d in directors:
        st.write(f"- {d['_id']} : {d['count']} films")
else:
    st.write(f"Aucun")


# Question 8
st.subheader("8. Quel est le genre de film qui rapporte en moyenne le plus de revenus ?")

# Question 9
st.subheader("9. Quels sont les 3 films les mieux notés (rating) pour chaque décennie (1990-1999, 2000-2009,etc.) ?")


# Question 10
st.subheader("10. Quel est le film le plus long (Runtime) par genre ?")

# Question 11
st.subheader("11. Créer une vue MongoDB affichant uniquement les films ayant une note supérieure à 80 (Metascore) et généré plus de 50 millions de dollars.")
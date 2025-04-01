import streamlit as st
# import des fonctions
from src.mongodb import getGetYearWithMostMovies, countMoviesAfter1999, averageVotes2007, getMoviesCountPerYear, getAllGenres, getHighestRevenueMovie, getDirectorsWithMoreThan5Movies, getGenreWithHighestAvgRevenue, getTop3RatedMoviesByDecade, getLongestMovieByGenre, getHighRatedAndProfitableMovies, getRuntimesAndRevenues, getAverageRuntimeByDecade
import matplotlib.pyplot as plt
import numpy as np
# import des fonctions
from src.neo4jdb import getActorWithMostMovie, getActorsWithAnneHathaway, getActorWithMostRevenue, getAvgVote, getMostRepresentedGenre, getFilmsWithCoactors, getDirectorWithMostActors, getActorsWithMostDirectors, recomMovieToActor, getShortestPathBetweenActors, getFilmsWithCommonGenres, recommendFilmsBasedOnActor, createCompetitionRelation, getFrequentCollaboration

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


top_genre = getGenreWithHighestAvgRevenue()
st.write(f"Le genre **{top_genre['_id']}** rapporte en moyenne **{top_genre['avg_revenue']:.2f} millions**.")


# Question 9
st.subheader("9. Quels sont les 3 films les mieux notés (rating) pour chaque décennie (1990-1999, 2000-2009,etc.) ?")

decennies = getTop3RatedMoviesByDecade()
for i in decennies:
    st.markdown(f"###Décennie : {i['decade']}")
    for movie in i["topMovies"]:
        st.write(f"- {movie['title']} ({movie['year']}) — {movie['rating']}")



# Question 10
st.subheader("10. Quel est le film le plus long (Runtime) par genre ?")
longest = getLongestMovieByGenre()
for film in longest:
    st.write(f"**{film['_id']}** : _{film['title']}_ ({film['runtime']} min)")

# Question 11
st.subheader("11. Créer une vue MongoDB affichant uniquement les films ayant une note supérieure à 80 (Metascore) et généré plus de 50 millions de dollars.")

movies = getHighRatedAndProfitableMovies()
for m in movies:
    st.write(f"{m['title']} — Metascore : {m['Metascore']} — {m['Revenue (Millions)']}")


# Question 12
st.subheader(" 12 Calculer la corrélation entre la durée des films (Runtime) et leur revenu (Revenue). (réaliser une analyse statistique.)")

datas = getRuntimesAndRevenues()
runtimes = [data["Runtime (Minutes)"] for data in datas]
revenues = [data["Revenue (Millions)"] for data in datas]

corr = np.corrcoef(runtimes, revenues)[0, 1]
st.write(f"Coefficient: **{corr:.2f}**")

plt.figure(figsize=(8, 5))
plt.scatter(runtimes, revenues)
plt.xlabel("Durée du film enminutes")
plt.ylabel("Revenu")
plt.title("Corrélation entre la durée et  revenu")
st.pyplot(plt)

if corr > 0.5:
    st.success("Corrélation positive, les films plus longs rapportent souvent plus.")
elif corr < -0.5:
    st.error("Corrélation négative les films plus longs rapportent souvent moins.")
else:
    st.info("Corrélation faible ou nulle, la durée n'influence pas")


# Question 13
st.subheader("13. Y a-t-il une évolution de la durée moyenne des films par décennie ?")

datas = getAverageRuntimeByDecade()
decennies = [str(data["_id"]) for data in datas]
runtimes = [data["average_runtime"] for data in datas]

plt.figure(figsize=(10, 4))
plt.plot(decennies, runtimes, marker='o')
plt.xlabel("Décennie")
plt.ylabel("Durée moyenne (minutes)")
plt.title("Durée moyenne des films par décennie")
st.pyplot(plt)

if runtimes[-1] > runtimes[0]:
    st.success("Les films sont en général plus longs qu’avant")


# QUestion 14
st.subheader("14. Quel est l’acteur ayant joué dans le plus grand nombre de films ?")
acteur, nb_films = getActorWithMostMovie()
st.write(f"L'acteur ayant joué dans le plus grand nombre de fil est {acteur}, il à joué dans {nb_films} films.")


# QUestion 15
st.subheader("15. Quels sont les acteurs ayant joué dans des films où l’actrice Anne Hathaway a également joué?")
acteurs = getActorsWithAnneHathaway()

st.write(f"Les acteurs ayant joué dans des films avec Anne Hathaway sont :")
for acteur in acteurs:
    st.write(f"- {acteur}")


# QUestion 16
st.subheader("16. Quel est l’acteur ayant joué dans des films totalisant le plus de revenus ?")
acteur, total_revenue = getActorWithMostRevenue()
st.write(f"L'acteur ayant joué dans des films totalisant le plus de revenus est {acteur}")


# QUestion 17
st.subheader("17. Quelle est la moyenne des votes ?")

moyenne_votes = getAvgVote()
st.write(f"La moyenne est {moyenne_votes}")

# QUestion 18
st.subheader("18. Quel est le genre le plus représenté dans la base de données ?")

genre, nb = getMostRepresentedGenre()
st.write(f"Le genre le plus représenté est {genre} avec {nb} films")


# QUestion 19
st.subheader("19. Quels sont les films dans lesquels les acteurs ayant joué avec vous ont également joué ?")

majid = "Majid"
films = getFilmsWithCoactors(actor_name=majid)

st.write(f"Les films dans lesquels les acteurs ayant joué avec moi (majid) ont également joué sont :")
for film in films:
    st.write(f"- {film}")

# QUestion 20
st.subheader("20. Quel réalisateur Director a travaillé avec le plus grand nombre d’acteurs distincts ?")
realisateur, nb_acteur = getDirectorWithMostActors()
st.write(f"Le réalisateur ayant travaillé avec le plus grand nombre d'acteurs distincts est {realisateur} avec {nb_acteur} acteurs.")


# QUestion 21
# st.subheader("21. Quels sont les films les plus ”connectés”, c’est-à-dire ceux qui ont le plus d’acteurs en commun avec d’autres films ?")

# QUestion 22
st.subheader("22. Trouver les 5 acteurs ayant joué avec le plus de réalisateurs différents.")

acteurs = getActorsWithMostDirectors()
for act, nb_realalisateur in acteurs:
    st.write(f"{act} a joué avec {nb_realalisateur} realisateurs différents")


# QUestion 23
st.subheader("23. Recommander un film à un acteur en fonction des genres des films où il a déjà joué.")

acteur = "Leonardo DiCaprio"
st.subheader(f"Avec {acteur}")
film, genre = recomMovieToActor(acteur=acteur)
st.write(f"Le film recommandé pour {acteur} est '{film}', de type : '{genre}'.")

# QUestion 24
st.subheader("24. Créer une relation INFLUENCE PAR entre les réalisateurs en se basant sur des similarités dans les genres de films qu’ils ont réalisés.")
st.write(f"ok")

# QUestion 25
st.subheader("25. Quel est le ”chemin” le plus court entre deux acteurs donnés (ex : Tom Hanks et Scarlett Johansson) ?")


acteur1 = "Tom Hanks"
acteur2 = "Scarlett Johansson"

path = getShortestPathBetweenActors(acteur1=acteur1, acteur2=acteur2)
st.write(f"Le chemin le plus court entre {acteur1} et {acteur2} est :")
st.write(" -> ".join(path))

# QUestion 26
# st.subheader("26. Analyser les communautés d’acteurs : Quels sont les groupes d’acteurs qui ont tendance à travailler ensemble ? (Utilisation d’algorithmes de détection de communauté comme Louvain.)")


st.subheader("27. Quels sont les films qui ont des genres en commun mais qui ont des réalisateurs différents ?")
films = getFilmsWithCommonGenres()

for film in films:
    st.write(f"**Film 1**: {film['film1']} | **Film 2**: {film['film2']} | Genre: {film['genre']} | **Directeur 1**: {film['director1']} | **Directeur 2**: {film['director2']}")


st.subheader("28. Recommander des films aux utilisateurs en fonction des préférences d’un acteur donné.")

actor_name = st.text_input("Entrez le nom de l'acteur", "Leonardo DiCaprio")
films = recommendFilmsBasedOnActor(actor_name=actor_name)

for film in films:
    st.write(f"**Film recommandé**: {film['recommended_film']} | Genre: {film['genre']}")


st.subheader("29. Créer une relation de ”concurrence” entre réalisateurs ayant réalisé des films similaires la même année.")

competitors = createCompetitionRelation()
for competitor in competitors:
    st.write(f"**Réalisateur 1**: {competitor['director1']} |**Réalisateur 2**: {competitor['director2']} | Année: {competitor['year']} | Genre: {competitor['genre']}")




st.subheader("30. Identifier les collaborations les plus fréquentes entre réalisateurs et acteurs, puis analyser si ces collaborations sont associées à un succès commercial ou critique")
collaborations = getFrequentCollaboration()

for collaboration in collaborations:
    st.write(f"**Réalisateur**: {collaboration['director']} | **Acteurs**: {collaboration['actor']} | Nb de collaborations: {collaboration['collaboration_count']}")

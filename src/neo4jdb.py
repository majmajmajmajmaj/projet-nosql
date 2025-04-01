from neo4j import GraphDatabase
import src.config as conf

# import des informations de connexion depuis le fichier src/config.py ou ils sont définies en dur.
uri = conf.NEO4J_URI
user = conf.NEO4J_USER
password = conf.NEO4J_PSSW

#  crée un objet driver qui permet d'interagir avec la bdd et ouvrir une session, driver est utilisé dans toutes les methodes effectuant des requêtes
driver = GraphDatabase.driver(uri, auth=(user, password))

# test de connexion
# def test_connexion():
#     with driver.session() as session:
#         result = session.run("RETURN 'OK' AS message")
#         for row in result:
#             print(row["message"])


# ------- Ci dessous toutes ces methodes retournent le resultat des requetes, elles sont ensuite appelées dans index.py afin d'afficher sur l'app. ----#

# Question 14
def getActorWithMostMovie(driver=driver):
    req = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)
    WITH a, count(f) AS nb_films
    ORDER BY nb_films DESC
    LIMIT 1
    RETURN a.name AS acteur, nb_films
    """
    with driver.session() as session:
        result = session.run(req)
        for row in result:
            return row["acteur"], row["nb_films"]

def getActorsWithAnneHathaway(driver=driver):
    req = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)<-[:A_JOUE]-(ah:Actor {name: "Anne Hathaway"})
    RETURN a.name AS acteur
    """
    with driver.session() as session:
        result = session.run(req)
        acteurs = [row["acteur"] for row in result]
    return acteurs



def getActorWithMostRevenue(driver=driver):
    req = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)
    WITH a, SUM(f.Revenue) AS total_revenue
    ORDER BY total_revenue DESC
    LIMIT 1
    RETURN a.name AS acteur, total_revenue
    """
    with driver.session() as session:
        result = session.run(req)
        for row in result:
            return row["acteur"], row["total_revenue"]
        


def getAvgVote(driver=driver):
    req = """
    MATCH (f:Film)
    RETURN AVG(COALESCE(f.votes, 0)) AS moyenne_votes
    """
    with driver.session() as session:
        result = session.run(req)
        for row in result:
            return row["moyenne_votes"]


def getMostRepresentedGenre(driver=driver):
    req = """
    MATCH (f:Film)
    UNWIND split(f.genre, ",") AS genre
    WITH genre, count(f) AS genre_count
    ORDER BY genre_count DESC
    LIMIT 1
    RETURN genre, genre_count
    """
    with driver.session() as session:
        result = session.run(req)
        for row in result:
            return row["genre"], row["genre_count"]
        

def getFilmsWithCoactors(driver=driver, actor_name="Majid"):
    req = f"""
    MATCH (actor:Actor {{name: "{actor_name}"}})-[:A_JOUE]->(f:Film)<-[:A_JOUE]-(coactor:Actor)
    WHERE actor <> coactor
    RETURN DISTINCT f.title AS film
    """
    with driver.session() as session:
        result = session.run(req)
        films = [row["film"] for row in result]
    return films


def getDirectorWithMostActors(driver=driver):
    req = """
    MATCH (d:Realisateur)-[:A_REALISE]->(f:Film)-[:A_JOUE]-(a:Actor)
    WITH d, COUNT(DISTINCT a) AS nb_actors
    ORDER BY nb_actors DESC
    LIMIT 1
    RETURN d.name AS realisateur, nb_actors
    """
    with driver.session() as session:
        result = session.run(req)
        for row in result:
            return row["realisateur"], row["nb_actors"]

def getActorsWithMostDirectors(driver=driver):
    req = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)-[:A_REALISE]->(r:Realisateur)
    WITH a.name AS acteur, COUNT(DISTINCT r) AS nb_real
    ORDER BY nb_real DESC
    LIMIT 5
    RETURN acteur, nb_real
    """
    with driver.session() as session:
        result = session.run(req)
        acteur = []
        for row in result:
            acteur.append((row["acteur"], row["nb_real"]))
        return acteur


def recomMovieToActor(driver=driver, acteur=""):
    req = """
    MATCH (a:Actor)-[:A_JOUE]->(f:Film), (f2:Film)
    WHERE a.name = $acteur
    AND f.genre IN f2.genre
    AND NOT (a)-[:A_JOUE]->(f2)
    RETURN f2.title AS film_recommande, f2.genre AS genre
    LIMIT 1
    """
    with driver.session() as session:
        result = session.run(req, {"acteur": acteur})
        row = result.single()
        return row["film_recommande"], row["genre"]
    


# Question 24
def createInfluenceRelationBetweenDirectors(driver=driver):
    req = """
    MATCH (r1:Realisateur)-[:A_REALISE]->(f1:Film), (r2:Realisateur)-[:A_REALISE]->(f2:Film)
    WHERE r1 <> r2 AND f1.genre = f2.genre
    MERGE (r1)-[:INFLUENCE_PAR]->(r2)
    """
    with driver.session() as session:
        session.run(req)

# Appel pour créer les relations
createInfluenceRelationBetweenDirectors(driver)

def getShortestPathBetweenActors(driver=driver, acteur1="Tom Hanks", acteur2="Scarlett Johansson"):
    req = """
    MATCH p = shortestPath((a1:Actor {name: $acteur1})-[:A_JOUE*]-(a2:Actor {name: $acteur2}))
    RETURN p
    """
    with driver.session() as session:
        result = session.run(req, {"acteur1": acteur1, "acteur2": acteur2})
        path = result.single()
        nodes = []
        for node in path["p"].nodes:
            nodes.append(node["name"] if "name" in node else "")
        return nodes

def getFilmsWithCommonGenres(driver=driver):
    req = """
    MATCH (f1:Film)-[:A_REALISE]->(r1:Realisateur), (f2:Film)-[:A_REALISE]->(r2:Realisateur)
    WHERE f1 <> f2 AND f1.genre = f2.genre AND r1 <> r2
    RETURN f1.title AS film1, f2.title AS film2, f1.genre AS genre, r1.name AS director1, r2.name AS director2
    ORDER BY f1.genre
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(req)
        films = []
        for row in result:
            films.append({
                "film1": row["film1"],
                "film2": row["film2"],
                "genre": row["genre"],
                "director1": row["director1"],
                "director2": row["director2"]
            })
        return films


def recommendFilmsBasedOnActor(driver=driver, actor_name="Leonardo DiCaprio"):
    req = f"""
    MATCH (a:Actor)-[:A_JOUE]->(f:Film)
    WHERE a.name = '{actor_name}'
    WITH DISTINCT f.genre AS genre, a
    MATCH (f2:Film)
    WHERE f2.genre = genre AND NOT (f2)<-[:A_JOUE]-(a)
    RETURN f2.title AS recommended_film, f2.genre AS genre
    ORDER BY f2.title
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(req)
        films = []
        for row in result:
            films.append({
                "recommended_film": row["recommended_film"],
                "genre": row["genre"]
            })
        return films


def createCompetitionRelation(driver=driver):
    req = """
    MATCH (r1:Realisateur)-[:A_REALISE]->(f1:Film), (r2:Realisateur)-[:A_REALISE]->(f2:Film)
    WHERE r1 <> r2 AND f1.year = f2.year AND f1.genre = f2.genre
    MERGE (r1)-[:CONCURRENCE]->(r2)
    RETURN r1.name AS director1, r2.name AS director2, f1.year AS year, f1.genre AS genre
    ORDER BY f1.year, f1.genre
    """
    with driver.session() as session:
        result = session.run(req)
        competitors = []
        for row in result:
            competitors.append({
                "director1": row["director1"],
                "director2": row["director2"],
                "year": row["year"],
                "genre": row["genre"]
            })
        return competitors
    

def getFrequentCollaboration(driver=driver):
    req = """
    MATCH (r:Realisateur)-[:A_REALISE]->(f:Film)<-[:A_JOUE]-(a:Actor)
    WITH r.name AS director, a.name AS actor, COUNT(f) AS collaboration_count, SUM(f.Revenue) AS total_revenue, AVG(f.Metascore) AS avg_metascore
    ORDER BY collaboration_count DESC
    LIMIT 10
    RETURN director, actor, collaboration_count, total_revenue, avg_metascore
    """
    with driver.session() as session:
        result = session.run(req)
        collaborations = []
        for row in result:
            collaborations.append({
                "director": row["director"],
                "actor": row["actor"],
                "collaboration_count": row["collaboration_count"],
                "total_revenue": row["total_revenue"],
                "avg_metascore": row["avg_metascore"]
            })
        return collaborations


from neo4j import GraphDatabase

# ─────────────────────────────────────────────
#  CONFIGURACIÓN DE CONEXIÓN
# ─────────────────────────────────────────────
URI      = "neo4j+s://9e57e680.databases.neo4j.io"
USERNAME = "javier.benitezgarcia112@gmail.com"
PASSWORD = "javiergamer112"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


# ══════════════════════════════════════════════════════════════════
#  INCISO 1 — Funciones para crear el grafo básico
#  (USER, MOVIE, relación RATED)
# ══════════════════════════════════════════════════════════════════

def crear_usuario(tx, user_id: str, name: str):
    """Crea o actualiza un nodo USER."""
    query = """
        MERGE (u:USER {userId: $userId})
        SET u.name = $name
        RETURN u
    """
    return tx.run(query, userId=user_id, name=name).single()


def crear_pelicula(tx, movie_id: int, title: str, year: int, plot: str):
    """Crea o actualiza un nodo MOVIE."""
    query = """
        MERGE (m:MOVIE {movieId: $movieId})
        SET m.title = $title,
            m.year  = $year,
            m.plot  = $plot
        RETURN m
    """
    return tx.run(query, movieId=movie_id, title=title, year=year, plot=plot).single()


def crear_rated(tx, user_id: str, movie_id: int, rating: int, timestamp: int):
    """Crea la relación RATED entre un USER y una MOVIE."""
    query = """
        MATCH (u:USER  {userId:  $userId})
        MATCH (m:MOVIE {movieId: $movieId})
        MERGE (u)-[r:RATED]->(m)
        SET r.rating    = $rating,
            r.timestamp = $timestamp
        RETURN u, r, m
    """
    return tx.run(query, userId=user_id, movieId=movie_id,
                  rating=rating, timestamp=timestamp).single()


# ══════════════════════════════════════════════════════════════════
#  INCISO 3 — Funciones de búsqueda
# ══════════════════════════════════════════════════════════════════

def encontrar_usuario(tx, user_id: str):
    """Retorna un usuario por su userId."""
    query = "MATCH (u:USER {userId: $userId}) RETURN u"
    return tx.run(query, userId=user_id).single()


def encontrar_pelicula(tx, movie_id: int):
    """Retorna una película por su movieId."""
    query = "MATCH (m:MOVIE {movieId: $movieId}) RETURN m"
    return tx.run(query, movieId=movie_id).single()


def encontrar_usuario_con_rating(tx, user_id: str):
    """Retorna un usuario con todas sus relaciones RATED hacia películas."""
    query = """
        MATCH (u:USER {userId: $userId})-[r:RATED]->(m:MOVIE)
        RETURN u.name   AS usuario,
               m.title  AS pelicula,
               r.rating AS rating,
               r.timestamp AS timestamp
        ORDER BY r.rating DESC
    """
    return tx.run(query, userId=user_id).data()


# ══════════════════════════════════════════════════════════════════
#  INCISO 4 — Funciones para el grafo extendido
#  (Person:Actor, Person:Director, Movie, Genre, User)
# ══════════════════════════════════════════════════════════════════

def crear_actor(tx, tmdb_id: int, name: str, born: str, died: str,
                born_in: str, url: str, imdb_id: int, bio: str, poster: str):
    """Crea o actualiza un nodo Person:Actor."""
    query = """
        MERGE (a:Person:Actor {tmdbId: $tmdbId})
        SET a.name   = $name,
            a.born   = date($born),
            a.died   = CASE WHEN $died IS NULL THEN null ELSE date($died) END,
            a.bornIn = $bornIn,
            a.url    = $url,
            a.imdbId = $imdbId,
            a.bio    = $bio,
            a.poster = $poster
        RETURN a
    """
    return tx.run(query, tmdbId=tmdb_id, name=name, born=born, died=died,
                  bornIn=born_in, url=url, imdbId=imdb_id, bio=bio, poster=poster).single()


def crear_director(tx, tmdb_id: int, name: str, born: str, died: str,
                   born_in: str, url: str, imdb_id: int, bio: str, poster: str):
    """Crea o actualiza un nodo Person:Director."""
    query = """
        MERGE (d:Person:Director {tmdbId: $tmdbId})
        SET d.name   = $name,
            d.born   = date($born),
            d.died   = CASE WHEN $died IS NULL THEN null ELSE date($died) END,
            d.bornIn = $bornIn,
            d.url    = $url,
            d.imdbId = $imdbId,
            d.bio    = $bio,
            d.poster = $poster
        RETURN d
    """
    return tx.run(query, tmdbId=tmdb_id, name=name, born=born, died=died,
                  bornIn=born_in, url=url, imdbId=imdb_id, bio=bio, poster=poster).single()


def crear_pelicula_extendida(tx, tmdb_id: int, title: str, released: str,
                              imdb_rating: float, movie_id: int, year: int,
                              imdb_id: int, runtime: int, countries: list,
                              imdb_votes: int, url: str, revenue: int,
                              plot: str, poster: str, budget: int,
                              languages: list):
    """Crea o actualiza un nodo Movie con todas sus propiedades."""
    query = """
        MERGE (m:Movie {movieId: $movieId})
        SET m.tmdbId     = $tmdbId,
            m.title      = $title,
            m.released   = date($released),
            m.imdbRating = $imdbRating,
            m.year       = $year,
            m.imdbId     = $imdbId,
            m.runtime    = $runtime,
            m.countries  = $countries,
            m.imdbVotes  = $imdbVotes,
            m.url        = $url,
            m.revenue    = $revenue,
            m.plot       = $plot,
            m.poster     = $poster,
            m.budget     = $budget,
            m.languages  = $languages
        RETURN m
    """
    return tx.run(query,
                  tmdbId=tmdb_id, title=title, released=released,
                  imdbRating=imdb_rating, movieId=movie_id, year=year,
                  imdbId=imdb_id, runtime=runtime, countries=countries,
                  imdbVotes=imdb_votes, url=url, revenue=revenue,
                  plot=plot, poster=poster, budget=budget,
                  languages=languages).single()


def crear_genero(tx, name: str):
    """Crea o actualiza un nodo Genre."""
    query = "MERGE (g:Genre {name: $name}) RETURN g"
    return tx.run(query, name=name).single()


def crear_usuario_extendido(tx, user_id: int, name: str):
    """Crea o actualiza un nodo User (grafo extendido, userId entero)."""
    query = """
        MERGE (u:User {userId: $userId})
        SET u.name = $name
        RETURN u
    """
    return tx.run(query, userId=user_id, name=name).single()


def crear_acted_in(tx, actor_tmdb_id: int, movie_id: int, role: str):
    """Crea la relación ACTED_IN entre un Actor y una Movie."""
    query = """
        MATCH (a:Person:Actor {tmdbId: $actorId})
        MATCH (m:Movie         {movieId: $movieId})
        MERGE (a)-[r:ACTED_IN]->(m)
        SET r.role = $role
        RETURN a, r, m
    """
    return tx.run(query, actorId=actor_tmdb_id, movieId=movie_id, role=role).single()


def crear_directed(tx, director_tmdb_id: int, movie_id: int, role: str):
    """Crea la relación DIRECTED entre un Director y una Movie."""
    query = """
        MATCH (d:Person:Director {tmdbId: $dirId})
        MATCH (m:Movie            {movieId: $movieId})
        MERGE (d)-[r:DIRECTED]->(m)
        SET r.role = $role
        RETURN d, r, m
    """
    return tx.run(query, dirId=director_tmdb_id, movieId=movie_id, role=role).single()


def crear_in_genre(tx, movie_id: int, genre_name: str):
    """Crea la relación IN_GENRE entre una Movie y un Genre."""
    query = """
        MATCH (m:Movie {movieId:  $movieId})
        MATCH (g:Genre {name: $genreName})
        MERGE (m)-[:IN_GENRE]->(g)
        RETURN m, g
    """
    return tx.run(query, movieId=movie_id, genreName=genre_name).single()


def crear_rated_extendido(tx, user_id: int, movie_id: int, rating: int, timestamp: int):
    """Crea la relación RATED entre un User y una Movie (grafo extendido)."""
    query = """
        MATCH (u:User  {userId:  $userId})
        MATCH (m:Movie {movieId: $movieId})
        MERGE (u)-[r:RATED]->(m)
        SET r.rating    = $rating,
            r.timestamp = $timestamp
        RETURN u, r, m
    """
    return tx.run(query, userId=user_id, movieId=movie_id,
                  rating=rating, timestamp=timestamp).single()


# ══════════════════════════════════════════════════════════════════
#  EJEMPLO DE USO — Llamadas de prueba para evidenciar el inciso 3
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    with driver.session() as session:

        # --- Ejemplo inciso 3: buscar usuario U001 ---
        u = session.execute_read(encontrar_usuario, "U001")
        print("Usuario:", dict(u["u"]) if u else "No encontrado")

        # --- Ejemplo inciso 3: buscar película movieId=1 ---
        m = session.execute_read(encontrar_pelicula, 1)
        print("Película:", dict(m["m"]) if m else "No encontrada")

        # --- Ejemplo inciso 3: usuario con sus ratings ---
        ratings = session.execute_read(encontrar_usuario_con_rating, "U001")
        for row in ratings:
            print(f"  {row['usuario']} → {row['pelicula']} | rating={row['rating']}")

    driver.close()
from neo4j import GraphDatabase


URI      = "neo4j+s://9e57e680.databases.neo4j.io"
USERNAME = "9e57e680"
PASSWORD = "mWbiLrtpYPMVZqsjOBsRhs5xjf8R3X9mG0HM6DqhK4o"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))


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
    return tx.run("MATCH (u:USER {userId: $userId}) RETURN u", userId=user_id).single()


def encontrar_pelicula(tx, movie_id: int):
    """Retorna una película por su movieId."""
    return tx.run("MATCH (m:MOVIE {movieId: $movieId}) RETURN m", movieId=movie_id).single()


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
# ══════════════════════════════════════════════════════════════════

def crear_actor(tx, tmdb_id: int, name: str, born: str, died,
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


def crear_director(tx, tmdb_id: int, name: str, born: str, died,
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
                              plot: str, poster: str, budget: int, languages: list):
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
    return tx.run(query, tmdbId=tmdb_id, title=title, released=released,
                  imdbRating=imdb_rating, movieId=movie_id, year=year,
                  imdbId=imdb_id, runtime=runtime, countries=countries,
                  imdbVotes=imdb_votes, url=url, revenue=revenue,
                  plot=plot, poster=poster, budget=budget, languages=languages).single()


def crear_genero(tx, name: str):
    """Crea o actualiza un nodo Genre."""
    return tx.run("MERGE (g:Genre {name: $name}) RETURN g", name=name).single()


def crear_usuario_extendido(tx, user_id: int, name: str):
    """Crea o actualiza un nodo User (grafo extendido)."""
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
#  MAIN — Poblar y demostrar (incisos 2, 3 y 4)
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    print("=" * 60)
    print("  LAB 08 — The Nodes World Cup Part I")
    print("=" * 60)

    with driver.session() as session:

        # ── INCISO 2: Poblar grafo básico ──────────────────────────
        print("\n[INCISO 2] Creando usuarios, películas y ratings...")

        usuarios = [
            ("U001", "Ana García"),
            ("U002", "Carlos López"),
            ("U003", "María Pérez"),
            ("U004", "José Martínez"),
            ("U005", "Lucía Ramírez"),
        ]
        for uid, name in usuarios:
            session.execute_write(crear_usuario, uid, name)
            print(f"  ✔ Usuario: {name}")

        peliculas = [
            (1, "Inception",       2010, "Un ladrón roba secretos desde los sueños."),
            (2, "The Matrix",      1999, "Un hacker descubre la verdad sobre su realidad."),
            (3, "Interstellar",    2014, "Astronautas viajan a través de un agujero de gusano."),
            (4, "The Dark Knight", 2008, "Batman enfrenta al Joker en Gotham City."),
            (5, "Parasite",        2019, "Una familia pobre se infiltra en una familia rica."),
            (6, "Spirited Away",   2001, "Una niña queda atrapada en un mundo espiritual."),
            (7, "The Godfather",   1972, "La historia de una poderosa familia mafiosa."),
        ]
        for mid, title, year, plot in peliculas:
            session.execute_write(crear_pelicula, mid, title, year, plot)
            print(f"  ✔ Película: {title}")

        ratings = [
            ("U001", 1, 5, 1700000001), ("U001", 3, 4, 1700000002),
            ("U002", 2, 5, 1700000003), ("U002", 4, 3, 1700000004),
            ("U003", 1, 3, 1700000005), ("U003", 5, 5, 1700000006), ("U003", 6, 4, 1700000007),
            ("U004", 7, 5, 1700000008), ("U004", 2, 4, 1700000009),
            ("U005", 3, 2, 1700000010), ("U005", 6, 5, 1700000011),
        ]
        for uid, mid, rat, ts in ratings:
            session.execute_write(crear_rated, uid, mid, rat, ts)
            print(f"  ✔ RATED: {uid} → movieId={mid} (rating={rat})")

        # ── INCISO 3: Demostrar búsquedas ──────────────────────────
        print("\n[INCISO 3] Demostrando funciones de búsqueda...")

        u = session.execute_read(encontrar_usuario, "U001")
        print(f"\n  encontrar_usuario('U001'):")
        print(f"     {dict(u['u'])}")

        m = session.execute_read(encontrar_pelicula, 1)
        print(f"\n  encontrar_pelicula(1):")
        print(f"     {dict(m['m'])}")

        rows = session.execute_read(encontrar_usuario_con_rating, "U001")
        print(f"\n  encontrar_usuario_con_rating('U001'):")
        for row in rows:
            print(f"     {row['usuario']} → {row['pelicula']} | rating={row['rating']} | ts={row['timestamp']}")

        # ── INCISO 4: Poblar grafo extendido ───────────────────────
        print("\n[INCISO 4] Creando grafo extendido...")

        # Géneros
        for g in ["Science Fiction", "Action", "Thriller", "Adventure", "Drama"]:
            session.execute_write(crear_genero, g)
            print(f" Género: {g}")

        # Actores
        actores = [
            (500, "Leonardo DiCaprio", "1974-11-11", None, "Los Angeles, USA",
             "https://www.themoviedb.org/person/6193", 138,
             "Actor estadounidense ganador del Oscar.",
             "https://image.tmdb.org/t/p/w500/wo2hJpn04vbtmh0B9utCFdsQhxM.jpg"),
            (501, "Keanu Reeves", "1964-09-02", None, "Beirut, Lebanon",
             "https://www.themoviedb.org/person/6384", 206,
             "Actor conocido por The Matrix y John Wick.",
             "https://image.tmdb.org/t/p/w500/4D0PpNI0kmP58hgrwGC3wCjxhnm.jpg"),
            (502, "Matthew McConaughey", "1969-11-04", None, "Uvalde, Texas, USA",
             "https://www.themoviedb.org/person/10297", 190,
             "Actor ganador del Oscar por Dallas Buyers Club.",
             "https://image.tmdb.org/t/p/w500/wJiGedOCZhwMx9DezY8uwbNxmAY.jpg"),
        ]
        for a in actores:
            session.execute_write(crear_actor, *a)
            print(f"Actor: {a[1]}")

        # Directores
        directores = [
            (600, "Christopher Nolan", "1970-07-30", None, "London, UK",
             "https://www.themoviedb.org/person/525", 634,
             "Director británico-estadounidense.",
             "https://image.tmdb.org/t/p/w500/xuAIuYSmsUzKlUMBFGVZaWsY3DZ.jpg"),
            (601, "Lana Wachowski", "1965-06-21", None, "Chicago, USA",
             "https://www.themoviedb.org/person/9340", 905,
             "Directora co-creadora de la trilogía The Matrix.",
             "https://image.tmdb.org/t/p/w500/8KKEP1aQkZvx9LoC7QCmZZg3FpF.jpg"),
        ]
        for d in directores:
            session.execute_write(crear_director, *d)
            print(f"Director: {d[1]}")

        # Películas extendidas
        peliculas_ext = [
            (27205, "Inception", "2010-07-16", 8.8, 101, 2010, 1375666, 148,
             ["USA", "UK"], 2200000, "https://www.themoviedb.org/movie/27205",
             836836967, "Un ladrón que roba secretos desde el subconsciente.",
             "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
             160000000, ["English", "Japanese", "French"]),
            (603, "The Matrix", "1999-03-31", 8.7, 102, 1999, 133093, 136,
             ["USA", "Australia"], 1800000, "https://www.themoviedb.org/movie/603",
             463517383, "Un hacker descubre la verdad sobre su realidad.",
             "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
             63000000, ["English"]),
            (157336, "Interstellar", "2014-11-07", 8.6, 103, 2014, 816692, 169,
             ["USA", "UK", "Canada"], 1700000, "https://www.themoviedb.org/movie/157336",
             701729206, "Astronautas viajan a través de un agujero de gusano.",
             "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
             165000000, ["English"]),
        ]
        for p in peliculas_ext:
            session.execute_write(crear_pelicula_extendida, *p)
            print(f"Movie extendida: {p[1]}")

        # Usuarios extendidos
        for uid, name in [(1, "Ana García"), (2, "Carlos López"), (3, "María Pérez")]:
            session.execute_write(crear_usuario_extendido, uid, name)
            print(f" User: {name}")

        # Relaciones ACTED_IN
        for actor_id, mid, role in [
            (500, 101, "Dom Cobb"),
            (501, 102, "Neo"),
            (502, 103, "Cooper"),
        ]:
            session.execute_write(crear_acted_in, actor_id, mid, role)
            print(f"ACTED_IN: actor {actor_id} → movie {mid} como '{role}'")

        # Relaciones DIRECTED
        for dir_id, mid, role in [
            (600, 101, "Director"),
            (601, 102, "Director"),
            (600, 103, "Director"),
        ]:
            session.execute_write(crear_directed, dir_id, mid, role)
            print(f"DIRECTED: director {dir_id} → movie {mid}")

        # Relaciones IN_GENRE
        for mid, genre in [
            (101, "Science Fiction"), (101, "Thriller"),
            (102, "Science Fiction"), (102, "Action"),
            (103, "Science Fiction"), (103, "Adventure"),
        ]:
            session.execute_write(crear_in_genre, mid, genre)
            print(f"IN_GENRE: movie {mid} → {genre}")

        # Relaciones RATED extendidas
        for uid, mid, rat, ts in [
            (1, 101, 5, 1700100001), (1, 103, 4, 1700100002),
            (2, 102, 5, 1700100003),
            (3, 101, 3, 1700100004), (3, 102, 4, 1700100005),
        ]:
            session.execute_write(crear_rated_extendido, uid, mid, rat, ts)
            print(f"RATED extendido: user {uid} → movie {mid} (rating={rat})")

    driver.close()
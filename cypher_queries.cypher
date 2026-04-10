
// ────────────────────────────────────────────────────────────────
//  INCISO 1 
// ────────────────────────────────────────────────────────────────

// Crear USER
MERGE (u:USER {userId: $userId})
SET u.name = $name
RETURN u;

// Crear MOVIE
MERGE (m:MOVIE {movieId: $movieId})
SET m.title = $title,
    m.year  = $year,
    m.plot  = $plot
RETURN m;

// Crear relación RATED entre USER y MOVIE
MATCH (u:USER  {userId:  $userId})
MATCH (m:MOVIE {movieId: $movieId})
MERGE (u)-[r:RATED]->(m)
SET r.rating    = $rating,
    r.timestamp = $timestamp
RETURN u, r, m;


// ────────────────────────────────────────────────────────────────
//  INCISO 2 
// ────────────────────────────────────────────────────────────────

// Usuarios
MERGE (:USER {userId:'U001', name:'Ana García'});
MERGE (:USER {userId:'U002', name:'Carlos López'});
MERGE (:USER {userId:'U003', name:'María Pérez'});
MERGE (:USER {userId:'U004', name:'José Martínez'});
MERGE (:USER {userId:'U005', name:'Lucía Ramírez'});

// Películas
MERGE (:MOVIE {movieId:1, title:'Inception',      year:2010, plot:'Un ladrón roba secretos desde los sueños.'});
MERGE (:MOVIE {movieId:2, title:'The Matrix',     year:1999, plot:'Un hacker descubre la verdad sobre su realidad.'});
MERGE (:MOVIE {movieId:3, title:'Interstellar',   year:2014, plot:'Astronautas viajan a través de un agujero de gusano.'});
MERGE (:MOVIE {movieId:4, title:'The Dark Knight',year:2008, plot:'Batman enfrenta al Joker en Gotham City.'});
MERGE (:MOVIE {movieId:5, title:'Parasite',       year:2019, plot:'Una familia pobre se infiltra en una familia rica.'});
MERGE (:MOVIE {movieId:6, title:'Spirited Away',  year:2001, plot:'Una niña queda atrapada en un mundo espiritual.'});
MERGE (:MOVIE {movieId:7, title:'The Godfather',  year:1972, plot:'La historia de una poderosa familia mafiosa.'});

// Relaciones RATED (Ana García)
MATCH (u:USER{userId:'U001'}),(m:MOVIE{movieId:1}) MERGE (u)-[:RATED {rating:5,timestamp:1700000001}]->(m);
MATCH (u:USER{userId:'U001'}),(m:MOVIE{movieId:3}) MERGE (u)-[:RATED {rating:4,timestamp:1700000002}]->(m);
// (Carlos López)
MATCH (u:USER{userId:'U002'}),(m:MOVIE{movieId:2}) MERGE (u)-[:RATED {rating:5,timestamp:1700000003}]->(m);
MATCH (u:USER{userId:'U002'}),(m:MOVIE{movieId:4}) MERGE (u)-[:RATED {rating:3,timestamp:1700000004}]->(m);
// (María Pérez)
MATCH (u:USER{userId:'U003'}),(m:MOVIE{movieId:1}) MERGE (u)-[:RATED {rating:3,timestamp:1700000005}]->(m);
MATCH (u:USER{userId:'U003'}),(m:MOVIE{movieId:5}) MERGE (u)-[:RATED {rating:5,timestamp:1700000006}]->(m);
MATCH (u:USER{userId:'U003'}),(m:MOVIE{movieId:6}) MERGE (u)-[:RATED {rating:4,timestamp:1700000007}]->(m);
// (José Martínez)
MATCH (u:USER{userId:'U004'}),(m:MOVIE{movieId:7}) MERGE (u)-[:RATED {rating:5,timestamp:1700000008}]->(m);
MATCH (u:USER{userId:'U004'}),(m:MOVIE{movieId:2}) MERGE (u)-[:RATED {rating:4,timestamp:1700000009}]->(m);
// (Lucía Ramírez)
MATCH (u:USER{userId:'U005'}),(m:MOVIE{movieId:3}) MERGE (u)-[:RATED {rating:2,timestamp:1700000010}]->(m);
MATCH (u:USER{userId:'U005'}),(m:MOVIE{movieId:6}) MERGE (u)-[:RATED {rating:5,timestamp:1700000011}]->(m);


// ────────────────────────────────────────────────────────────────
//  INCISO 3 
// ────────────────────────────────────────────────────────────────

// 3A) Encontrar un usuario por userId
MATCH (u:USER {userId: 'U001'})
RETURN u;

// 3B) Encontrar una película por movieId
MATCH (m:MOVIE {movieId: 1})
RETURN m;

// 3C) Encontrar usuario CON su relación RATED hacia películas
MATCH (u:USER {userId: 'U001'})-[r:RATED]->(m:MOVIE)
RETURN u.name   AS usuario,
       m.title  AS pelicula,
       r.rating AS rating,
       r.timestamp AS timestamp
ORDER BY r.rating DESC;


// ────────────────────────────────────────────────────────────────
//  INCISO 4 
// ────────────────────────────────────────────────────────────────

// ── Géneros ──
MERGE (:Genre {name:'Science Fiction'});
MERGE (:Genre {name:'Action'});
MERGE (:Genre {name:'Thriller'});
MERGE (:Genre {name:'Adventure'});

// ── Actores (Person:Actor) ──
MERGE (:Person:Actor {
    tmdbId:500, name:'Leonardo DiCaprio',
    born:date('1974-11-11'), bornIn:'Los Angeles, USA',
    url:'https://www.themoviedb.org/person/6193',
    imdbId:138, bio:'Actor estadounidense ganador del Oscar.',
    poster:'https://image.tmdb.org/t/p/w500/wo2hJpn04vbtmh0B9utCFdsQhxM.jpg'
});

MERGE (:Person:Actor {
    tmdbId:501, name:'Keanu Reeves',
    born:date('1964-09-02'), bornIn:'Beirut, Lebanon',
    url:'https://www.themoviedb.org/person/6384',
    imdbId:206, bio:'Actor conocido por The Matrix y John Wick.',
    poster:'https://image.tmdb.org/t/p/w500/4D0PpNI0kmP58hgrwGC3wCjxhnm.jpg'
});

MERGE (:Person:Actor {
    tmdbId:502, name:'Matthew McConaughey',
    born:date('1969-11-04'), bornIn:'Uvalde, Texas, USA',
    url:'https://www.themoviedb.org/person/10297',
    imdbId:190, bio:'Actor ganador del Oscar por Dallas Buyers Club.',
    poster:'https://image.tmdb.org/t/p/w500/wJiGedOCZhwMx9DezY8uwbNxmAY.jpg'
});

// ── Directores (Person:Director) ──
MERGE (:Person:Director {
    tmdbId:600, name:'Christopher Nolan',
    born:date('1970-07-30'), bornIn:'London, UK',
    url:'https://www.themoviedb.org/person/525',
    imdbId:634, bio:'Director británico-estadounidense.',
    poster:'https://image.tmdb.org/t/p/w500/xuAIuYSmsUzKlUMBFGVZaWsY3DZ.jpg'
});

MERGE (:Person:Director {
    tmdbId:601, name:'Lana Wachowski',
    born:date('1965-06-21'), bornIn:'Chicago, USA',
    url:'https://www.themoviedb.org/person/9340',
    imdbId:905, bio:'Directora co-creadora de la trilogía The Matrix.',
    poster:'https://image.tmdb.org/t/p/w500/8KKEP1aQkZvx9LoC7QCmZZg3FpF.jpg'
});

// ── Películas extendidas (Movie) ──
MERGE (m:Movie {movieId:101})
SET m.tmdbId=27205, m.title='Inception',
    m.released=date('2010-07-16'), m.imdbRating=8.8,
    m.year=2010, m.imdbId=1375666, m.runtime=148,
    m.countries=['USA','UK'], m.imdbVotes=2200000,
    m.url='https://www.themoviedb.org/movie/27205',
    m.revenue=836836967,
    m.plot='Un ladrón que roba secretos desde el subconsciente.',
    m.poster='https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg',
    m.budget=160000000, m.languages=['English','Japanese','French'];

MERGE (m:Movie {movieId:102})
SET m.tmdbId=603, m.title='The Matrix',
    m.released=date('1999-03-31'), m.imdbRating=8.7,
    m.year=1999, m.imdbId=133093, m.runtime=136,
    m.countries=['USA','Australia'], m.imdbVotes=1800000,
    m.url='https://www.themoviedb.org/movie/603',
    m.revenue=463517383,
    m.plot='Un hacker descubre la verdad sobre su realidad.',
    m.poster='https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg',
    m.budget=63000000, m.languages=['English'];

MERGE (m:Movie {movieId:103})
SET m.tmdbId=157336, m.title='Interstellar',
    m.released=date('2014-11-07'), m.imdbRating=8.6,
    m.year=2014, m.imdbId=816692, m.runtime=169,
    m.countries=['USA','UK','Canada'], m.imdbVotes=1700000,
    m.url='https://www.themoviedb.org/movie/157336',
    m.revenue=701729206,
    m.plot='Astronautas viajan a través de un agujero de gusano.',
    m.poster='https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
    m.budget=165000000, m.languages=['English'];

// ── Usuarios (User) ──
MERGE (:User {userId:1, name:'Ana García'});
MERGE (:User {userId:2, name:'Carlos López'});
MERGE (:User {userId:3, name:'María Pérez'});

// ── Relaciones ACTED_IN ──
MATCH (a:Person:Actor {tmdbId:500}),(m:Movie {movieId:101})
MERGE (a)-[:ACTED_IN {role:'Dom Cobb'}]->(m);

MATCH (a:Person:Actor {tmdbId:501}),(m:Movie {movieId:102})
MERGE (a)-[:ACTED_IN {role:'Neo'}]->(m);

MATCH (a:Person:Actor {tmdbId:502}),(m:Movie {movieId:103})
MERGE (a)-[:ACTED_IN {role:'Cooper'}]->(m);

// ── Relaciones DIRECTED ──
MATCH (d:Person:Director {tmdbId:600}),(m:Movie {movieId:101})
MERGE (d)-[:DIRECTED {role:'Director'}]->(m);

MATCH (d:Person:Director {tmdbId:601}),(m:Movie {movieId:102})
MERGE (d)-[:DIRECTED {role:'Director'}]->(m);

MATCH (d:Person:Director {tmdbId:600}),(m:Movie {movieId:103})
MERGE (d)-[:DIRECTED {role:'Director'}]->(m);

// ── Relaciones IN_GENRE ──
MATCH (m:Movie {movieId:101}),(g:Genre {name:'Science Fiction'}) MERGE (m)-[:IN_GENRE]->(g);
MATCH (m:Movie {movieId:101}),(g:Genre {name:'Thriller'})        MERGE (m)-[:IN_GENRE]->(g);
MATCH (m:Movie {movieId:102}),(g:Genre {name:'Science Fiction'}) MERGE (m)-[:IN_GENRE]->(g);
MATCH (m:Movie {movieId:102}),(g:Genre {name:'Action'})          MERGE (m)-[:IN_GENRE]->(g);
MATCH (m:Movie {movieId:103}),(g:Genre {name:'Science Fiction'}) MERGE (m)-[:IN_GENRE]->(g);
MATCH (m:Movie {movieId:103}),(g:Genre {name:'Adventure'})       MERGE (m)-[:IN_GENRE]->(g);

// ── Relaciones RATED (User → Movie) ──
MATCH (u:User {userId:1}),(m:Movie {movieId:101}) MERGE (u)-[:RATED {rating:5,timestamp:1700100001}]->(m);
MATCH (u:User {userId:1}),(m:Movie {movieId:103}) MERGE (u)-[:RATED {rating:4,timestamp:1700100002}]->(m);
MATCH (u:User {userId:2}),(m:Movie {movieId:102}) MERGE (u)-[:RATED {rating:5,timestamp:1700100003}]->(m);
MATCH (u:User {userId:3}),(m:Movie {movieId:101}) MERGE (u)-[:RATED {rating:3,timestamp:1700100004}]->(m);
MATCH (u:User {userId:3}),(m:Movie {movieId:102}) MERGE (u)-[:RATED {rating:4,timestamp:1700100005}]->(m);


// ────────────────────────────────────────────────────────────────
//  VERIFICACIÓN — Queries para confirmar que todo quedó bien
// ────────────────────────────────────────────────────────────────

// Ver todo el grafo básico
MATCH (n) RETURN n LIMIT 50;

// Ver todos los ratings del grafo básico
MATCH (u:USER)-[r:RATED]->(m:MOVIE)
RETURN u.name, m.title, r.rating ORDER BY u.name;

// Ver el grafo extendido completo
MATCH p=()-[]->() RETURN p LIMIT 100;

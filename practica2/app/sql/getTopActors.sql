-- Elena Cano Castillejo y Paula Samper López
-- Archivo getTopActors.sql


-- Actores que más han actuado en un género, de mas a menos
-- siempre que hayan trabajado en más de 4 películas de ese género


CREATE
OR REPLACE FUNCTION getTopActors(
    genre CHAR,
    OUT Actor char,
    OUT Num INT,
    OUT Debut INT,
    OUT Film CHAR,
    OUT Director CHAR
) RETURNS SETOF RECORD AS $$ 

BEGIN

DROP VIEW IF EXISTS ActorGeneroPart;
DROP VIEW IF EXISTS ActorGeneroDeb;


-- view con el id de cada actor, un genero, y su numero de participaciones 
-- en peliculas de dicho genero siempre que hayan sido >= 4

CREATE VIEW ActorGeneroPart AS

SELECT
    AM.actorid as actorid,
    MG.genre as genre,
    COUNT (DISTINCT AM.movieid) as participation
FROM
    public.imdb_actormovies as AM
    INNER JOIN public.imdb_moviegenres as MG ON AM.movieid = MG.movieid
GROUP BY
    AM.actorid,
    MG.genre
HAVING
    COUNT (DISTINCT AM.movieid) >= 4;


--view con los debut (Fecha y pelicula(s)) para cada actor-genero

CREATE VIEW ActorGeneroDeb AS

SELECT
    *
FROM
    (
        -- ordenar por fecha mas antigua para cada actor y genero
        -- si hay varias movieid debut (mismo año), se les asigna el mismo rango 
        SELECT
            AM.actorid as actorid,
            MG.genre as genre,
            AM.movieid as movieid,
            M.year as fecha,
            -- ordena de menor a mayor las fechas dependiendo del actor y el genero
            -- rango se reinicia cada vez que el actor o el genero cambian
            RANK() OVER (
                PARTITION BY AM.actorid,
                MG.genre
                ORDER BY
                    M.year ASC
            ) as rango
        FROM
            public.imdb_actormovies as AM
            INNER JOIN public.imdb_movies as M ON AM.movieid = M.movieid
            INNER JOIN public.imdb_moviegenres as MG ON MG.movieid = AM.movieid
    ) as ActorGeneroFechas
WHERE
    -- elegir la fecha mas antigua para cada actor-genero
    rango = 1;


-- salida: obtener los datos de la tabla y filtrar por el genero
RETURN QUERY (

SELECT
    CAST(A.actorname AS bpchar) as Actor,
    CAST(ActorGeneroPart.participation AS INT) as Num,
    CAST(ActorGeneroDeb.fecha AS INT) as Debut,
    CAST(M.movietitle AS bpchar) as Film,
    CAST(D.directorname AS bpchar) as Director
FROM
    ActorGeneroPart 
    -- participacion y debut
    INNER JOIN ActorGeneroDeb ON ActorGeneroPart.actorid = ActorGeneroDeb.actorid 
            AND ActorGeneroPart.genre = ActorGeneroDeb.genre
    -- nombre actor
    INNER JOIN public.imdb_actors as A on ActorGeneroDeb.actorid = A.actorid 
    -- nombre pelicula
    INNER JOIN public.imdb_movies as M on ActorGeneroDeb.movieid = M.movieid 
    -- nombre director
    -- puede haber varios, se desdoblan filas
    INNER JOIN public.imdb_directormovies as DM on ActorGeneroDeb.movieid = DM.movieid
    INNER JOIN public.imdb_directors as D on DM.directorid = D.directorid 
-- Donde el genero coincida
WHERE
    -- preguntar esto que no estoy muy segur
    ActorGeneroDeb.genre = $1
);


DROP VIEW IF EXISTS ActorGeneroPart;
DROP VIEW IF EXISTS ActorGeneroDeb;

END;

$$ LANGUAGE plpgsql;






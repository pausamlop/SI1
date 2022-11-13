-- Elena Cano Castillejo y Paula Samper López
-- Archivo getTopActors.sql


-- Actores que más han actuado en un género, de mas a menos
-- siempre que hayan trabajado en más de 4 películas de ese género



SELECT public.imdb_actorname, public.imdb_moviegenres.genre, count(distinct public.imdb_movies.movieid)
FROM imdb_actormovies INNER JOIN 

WHERE 



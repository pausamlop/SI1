-- Elena Cano Castillejo y Paula Samper López
-- Archivo updRatings.sql



-- actualizar la tabla imdb_movies cuando se añada, actualice  elimine una valoracion

-- funcion que ejecuta el trigger
CREATE
OR REPLACE FUNCTION updRatings() RETURNS TRIGGER AS $$ 

BEGIN


-- se añade una valoracion
IF (TG_OP = 'INSERT') THEN

    -- rating count
    UPDATE
        public.imdb_movies
    SET
        ratingcount = ratingcount + 1
    WHERE movieid = NEW.movieid;
    
    -- rating mean
    UPDATE
        public.imdb_movies
    SET
        ratingmean = round((ratingmean*(ratingcount-1) + NEW.rating)/ratingcount, 2)
    WHERE movieid = NEW.movieid;


-- se elimina una valoracion
ELSIF (TG_OP = 'DELETE') THEN

    -- rating count
    UPDATE
        public.imdb_movies
    SET
        ratingcount = ratingcount - 1
    WHERE movieid = NEW.movieid;

    -- rating mean (dos updates para evitar una division entre 0)
    UPDATE
        public.imdb_movies
    SET
        ratingmean = round((ratingmean*(ratingcount+1) - OLD.rating)/ratingcount, 2)
    WHERE 
        not ratingcount = 0 AND movieid = NEW.movieid;

    UPDATE
        public.imdb_movies
    SET
        ratingmean = 0
    WHERE 
        ratingcount = 0 AND movieid = NEW.movieid;



-- se actualiza una valoracion
ELSIF (TG_OP = 'UPDATE') THEN
    UPDATE
        public.imdb_movies
    SET
        -- rating mean
        ratingmean = ratingmean - OLD.rating + NEW.rating
    WHERE
        movieid = NEW.movieid;


END IF;

RETURN NULL;

END;

$$ LANGUAGE plpgsql;


-- trigger
CREATE OR REPLACE TRIGGER UR AFTER
INSERT OR DELETE OR UPDATE
    ON public.ratings FOR EACH ROW EXECUTE PROCEDURE updRatings();


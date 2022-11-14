-- Elena Cano Castillejo y Paula Samper López
-- Archivo updRatings.sql




-- actualizar la tabla imdb_movies cuando se añada, actualice  elimine una valoracion

-- funcion que ejecuta el trigger
CREATE
OR REPLACE FUNCTION updRatings() RETURNS TRIGGER AS $$ 

BEGIN


-- se añade una valoracion
IF (TG_OP = 'INSERT') THEN
    UPDATE
        public.imdb_movies
    SET
        -- rating mean
        -- ratingmean = round((ratingmean*ratingcount + NEW.rating)/(UNO+ratingcount), 2),
        -- rating count
        ratingcount = ratingcount + 1;


-- se elimina una valoracion
ELSIF (TG_OP = 'DELETE') THEN
    UPDATE
        public.imdb_movies
    SET
        -- rating mean
        -- ratingmean = round((ratingmean*ratingcount - OLD.rating)/(ratingcount -UNO), 2),
        -- rating count
        ratingcount = ratingcount - 1;


-- se actualiza una valoracion
ELSIF (TG_OP = 'UPDATE') THEN
    UPDATE
        public.imdb_movies
    SET
        -- rating mean
        ratingmean = ratingmean - OLD.rating + NEW.rating;


END IF;

RETURN NULL;

END;

$$ LANGUAGE plpgsql;



-- trigger
CREATE OR REPLACE TRIGGER UR AFTER
INSERT OR DELETE OR UPDATE
    ON public.ratings FOR EACH ROW EXECUTE PROCEDURE updRatings();


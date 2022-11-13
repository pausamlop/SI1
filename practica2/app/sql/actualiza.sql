-- Elena Cano Castillejo y Paula Samper López
-- Archivo actualiza.sql



----------------------  COMPLETAR ASPECTOS DE LA TABLA  ----------------------



---------------------------- añadir foreign keys -----------------------------


-- imdb_actormovies:    actorid --> imdb_actors
ALTER TABLE
    public.imdb_actormovies
ADD
    CONSTRAINT fk_actorid FOREIGN KEY (actorid) REFERENCES public.imdb_actors (actorid);


-- imdb_actormovies:    movieid --> imdb_movies
ALTER TABLE
    public.imdb_actormovies
ADD
    CONSTRAINT fk_movieid FOREIGN KEY (movieid) REFERENCES public.imdb_movies (movieid);


-- orderdetail:     orderid --> orders
ALTER TABLE
    public.orderdetail
ADD
    CONSTRAINT fk_orderid FOREIGN KEY (orderid) REFERENCES public.orders (orderid);


-- orderdetail:     prod_id --> product
ALTER TABLE
    public.orderdetail
ADD
    CONSTRAINT fk_prodid2 FOREIGN KEY (prod_id) REFERENCES public.products (prod_id);


-- inventory:      prod_id -> products
ALTER TABLE
    public.inventory
ADD
    CONSTRAINT fk_prodid1 FOREIGN KEY (prod_id) REFERENCES public.products (prod_id);


-- orders:      customerid -> customers
ALTER TABLE
    public.orders
ADD
    CONSTRAINT fk_customerid FOREIGN KEY (customerid) REFERENCES public.customers (customerid);


------------------------------------------------------------------------------


-- añadir triggers




-- añadir campo balance en la tabla customer para guardar el saldo
ALTER TABLE
    public.customers
ADD
    balance NUMERIC;
-- inicializar el campo a 0 para operar
UPDATE
    public.customers
SET
    balance = 0;


-- tabla ratings para guardar la valoracion de un usuario a una pelicula (y que no la valore 2 veces)
CREATE TABLE public.ratings (
    movieid integer REFERENCES public.imdb_movies (movieid),
    customerid integer REFERENCES public.customers (customerid),
    rating NUMERIC,
    PRIMARY KEY (movieid, customerid)
);


-- Añadir dos campos a la tabla ‘imdb_movies’, para contener la valoración media ‘ratingmean’ 
-- y el número de valoraciones ‘ratingcount’, de cada película.
ALTER TABLE
    public.imdb_movies
ADD
    ratingmean NUMERIC,
ADD
    ratingcount smallint;
-- inicializar los campos a 0 para poder operar
UPDATE
    public.imdb_movies
SET
    ratingmean = 0,
    ratingcount = 0;


-- Aumentar el tamaño de ‘password’ en la tabla ‘customers’ (96 caracteres hexadecimales)
ALTER TABLE
    public.customers
ALTER public.customers.password varbinary(96)








-- INSERT INTO public.imdb_actormovies_v1
-- SELECT * FROM public.imdb_actormovies

-- SELECT * FROM public.imdb_actormovies_v1
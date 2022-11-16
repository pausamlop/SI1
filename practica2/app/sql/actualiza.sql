-- Elena Cano Castillejo y Paula Samper López
-- Archivo actualiza.sql



----------------------  COMPLETAR ASPECTOS DE LA TABLA  ----------------------


------------------------- añadir cambios en cascada --------------------------

-- si se borra una pelicula -> borrar entrada en movie countries
ALTER TABLE
    public.imdb_moviecountries 
DROP 
    CONSTRAINT imdb_moviecountries_movieid_fkey,
ADD
    CONSTRAINT imdb_moviecountries_movieid_fkey FOREIGN KEY (movieid) 
    REFERENCES public.imdb_movies (movieid) ON DELETE CASCADE;

-- si se borra una pelicula -> borrar entrada en movie languages
ALTER TABLE
    public.imdb_movielanguages
DROP 
    CONSTRAINT imdb_movielanguages_movieid_fkey,
ADD
    CONSTRAINT imdb_movielanguages_movieid_fkey FOREIGN KEY (movieid) 
    REFERENCES public.imdb_movies (movieid) ON DELETE CASCADE;

-- si se borra una pelicula -> borrar entrada en movie genres
ALTER TABLE
    public.imdb_moviegenres
DROP 
    CONSTRAINT imdb_moviegenres_movieid_fkey,
ADD
    CONSTRAINT imdb_moviegenres_movieid_fkey FOREIGN KEY (movieid) 
    REFERENCES public.imdb_movies (movieid) ON DELETE CASCADE;


-- si se borra una pelicula -> borrar entrada en director movies
ALTER TABLE
    public.imdb_directormovies
DROP 
    CONSTRAINT imdb_directormovies_directorid_fkey,
ADD
    CONSTRAINT imdb_directormovies_movieid_fkey1 FOREIGN KEY (movieid) 
    REFERENCES public.imdb_movies (movieid) ON DELETE CASCADE;

-- si se borra una pelicula -> borrar products
ALTER TABLE
    public.products
DROP 
    CONSTRAINT products_movieid_fkey,
ADD
    CONSTRAINT products_movieid_fkey FOREIGN KEY (movieid) 
    REFERENCES public.imdb_movies (movieid) ON DELETE CASCADE;



------------------------------- constraints ---------------------------------



---------------------------- añadir foreign keys -----------------------------


-- imdb_actormovies:    actorid --> imdb_actors
ALTER TABLE
    public.imdb_actormovies
ADD
    CONSTRAINT fk_actorid FOREIGN KEY (actorid) 
    REFERENCES public.imdb_actors (actorid);


-- imdb_actormovies:    movieid --> imdb_movies
ALTER TABLE
    public.imdb_actormovies
ADD
    CONSTRAINT fk_movieid FOREIGN KEY (movieid) 
    REFERENCES public.imdb_movies (movieid) ON DELETE CASCADE;


-- orderdetail:     orderid --> orders
ALTER TABLE
    public.orderdetail
ADD
    CONSTRAINT fk_orderid FOREIGN KEY (orderid) 
    REFERENCES public.orders (orderid) ON DELETE CASCADE;


-- orderdetail:     prod_id --> product
ALTER TABLE
    public.orderdetail
ADD
    CONSTRAINT fk_prodid2 FOREIGN KEY (prod_id) 
    REFERENCES public.products (prod_id);


-- inventory:      prod_id -> products
ALTER TABLE
    public.inventory
ADD
    CONSTRAINT fk_prodid1 FOREIGN KEY (prod_id) 
    REFERENCES public.products (prod_id);


-- orders:      customerid -> customers
ALTER TABLE
    public.orders
ADD
    CONSTRAINT fk_customerid FOREIGN KEY (customerid) 
    REFERENCES public.customers (customerid);


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
    movieid integer REFERENCES public.imdb_movies (movieid) ON DELETE CASCADE,
    customerid integer REFERENCES public.customers (customerid),
    rating NUMERIC,
    PRIMARY KEY (movieid, customerid)
);


-- Añadir dos campos a la tabla ‘imdb_movies’, para contener la valoración media ‘ratingmean’ 
-- y el número de valoraciones ‘ratingcount’, de cada película.
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


-- Aumentar el tamaño de ‘password’ en la tabla ‘customers’ (96 caracteres hexadecimales)
ALTER TABLE
    public.customers
ADD
    COLUMN passhex varchar(96);

UPDATE
    public.customers
SET
    passhex = password;

ALTER TABLE
    public.customers DROP COLUMN password;

ALTER TABLE
    public.customers RENAME COLUMN passhex to password;





-- Funcion para inicializar el campo ‘balance’ de la tabla ‘customers’ a un número aleatorio entre 0 y N,
CREATE OR REPLACE 
FUNCTION setCustomersBalance(IN initialBalance bigint) 
RETURNS void as 
$$
UPDATE
    public.customers
SET
    balance = floor(initialBalance * random()) 
$$ LANGUAGE sql;

-- llamada a la funcion para N = 100
SELECT setCustomersBalance(100);





-----------------------------------INTEGRIDAD DE LOS DATOS----------------------------------



----------1. Para imdb_moviecountries---------------

--Creamos la tabla vacia 
CREATE TABLE public.imdb_countries (
    countryid INT GENERATED ALWAYS AS IDENTITY, 
    country varchar (32) not null,
    PRIMARY KEY (countryid)
    
);

--Añadimos los paises de las peliculas a la tabla creada
INSERT INTO public.imdb_countries (country)
SELECT DISTINCT country 
FROM imdb_moviecountries
ORDER BY country;


--Añadimos a imdb_moviecountries la nueva columna
ALTER TABLE imdb_moviecountries
ADD countryid INT;

--Ponemos a 0 la columna (por si acaso)
UPDATE public.imdb_moviecountries
SET countryid = 0;


--Poblamos la nueva columna
UPDATE public.imdb_moviecountries
SET countryid = A.countryid
FROM public.imdb_countries as A 
    INNER JOIN public.imdb_moviecountries as B on A.country = B.country
WHERE imdb_moviecountries.country = A.country;


--Eliminamos la column country
ALTER TABLE public.imdb_moviecountries DROP COLUMN country;

--Creamos una nueva primary key para relacionar imdb_moviecountries 
ALTER TABLE public.imdb_moviecountries
ADD CONSTRAINT imdb_moviecountries_pkey PRIMARY KEY (movieid, countryid);


--Creamos una nueva foregin key para relacionar imdb_moviecountries con moviecountries
ALTER TABLE public.imdb_moviecountries
ADD CONSTRAINT fk_countryid FOREIGN KEY (countryid) REFERENCES public.imdb_countries (countryid);







-------------2. Para imdb_moviegenres---------------

--Creamos la tabla vacia 
CREATE TABLE public.imdb_genres (
    genreid INT GENERATED ALWAYS AS IDENTITY, 
    genre varchar (32) not null,
    PRIMARY KEY (genreid)
    
);

--Añadimos los paises de las peliculas a la tabla creada
INSERT INTO public.imdb_genres (genre)
SELECT DISTINCT genre
FROM imdb_moviegenres
ORDER BY genre;


--Añadimos a imdb_moviecountries la nueva columna
ALTER TABLE imdb_moviegenres
ADD genreid INT;

--Ponemos a 0 la columna (por si acaso)
UPDATE public.imdb_moviegenres
SET genreid = 0;


--Poblamos la nueva columna
UPDATE public.imdb_moviegenres
SET genreid = A.genreid
FROM public.imdb_genres as A 
    INNER JOIN public.imdb_moviegenres as B on A.genre = B.genre
WHERE imdb_moviegenres.genre = A.genre;


--Eliminamos la column country
ALTER TABLE public.imdb_moviegenres DROP COLUMN genre;

--Creamos una nueva primary key para relacionar imdb_moviecountries 
ALTER TABLE public.imdb_moviegenres
ADD CONSTRAINT imdb_moviegenres_pkey PRIMARY KEY (movieid, genreid);


--Creamos una nueva foregin key para relacionar imdb_moviecountries con moviecountries
ALTER TABLE public.imdb_moviegenres
ADD CONSTRAINT fk_genreid FOREIGN KEY (genreid) REFERENCES public.imdb_genres (genreid);




-------------3. Para imdb_movielanguages---------------

--Creamos la tabla vacia 
CREATE TABLE public.imdb_languages (
    languageid INT GENERATED ALWAYS AS IDENTITY, 
    language varchar (32) not null,
    PRIMARY KEY (languageid)
    
);

--Añadimos los paises de las peliculas a la tabla creada
INSERT INTO public.imdb_languages (language)
SELECT DISTINCT language
FROM imdb_movielanguages
ORDER BY language;


--Añadimos a imdb_moviecountries la nueva columna
ALTER TABLE imdb_movielanguages
ADD languageid INT;

--Ponemos a 0 la columna (por si acaso)
UPDATE public.imdb_movielanguages
SET languageid = 0;


--Poblamos la nueva columna
UPDATE public.imdb_movielanguages
SET languageid = A.languageid
FROM public.imdb_languages as A 
    INNER JOIN public.imdb_movielanguages as B on A.language = B.language
WHERE imdb_movielanguages.language = A.language;


--Eliminamos la column country
ALTER TABLE public.imdb_movielanguages DROP COLUMN language;

--Creamos una nueva primary key para relacionar imdb_moviecountries 
ALTER TABLE public.imdb_movielanguages
ADD CONSTRAINT imdb_movielanguages_pkey PRIMARY KEY (movieid, languageid);


--Creamos una nueva foregin key para relacionar imdb_moviecountries con moviecountries
ALTER TABLE public.imdb_movielanguages
ADD CONSTRAINT fk_languageid FOREIGN KEY (languageid) REFERENCES public.imdb_languages (languageid);

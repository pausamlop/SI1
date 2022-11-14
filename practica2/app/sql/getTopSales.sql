-- Elena Cano Castillejo y Paula Samper López
-- Archivo getTopSales.sql

-- Pelicula mas vendida cada año entre dos años
-- Devuelve Year, Film, Sales, ordenado segun la cantidad

-- crear procedimiento
CREATE
OR REPLACE FUNCTION getTopSales(
    year1 INT,
    year2 INT,
    OUT Year INT,
    OUT Film CHAR,
    OUT sales bigint
) RETURNS SETOF RECORD AS $$ 

BEGIN 

-- Entradas de Year, Film, Sales, para todos los años y peliculas
CREATE VIEW SalesPerYear AS
SELECT
    EXTRACT(year FROM public.orders.orderdate) as yeardate,
    public.imdb_movies.movietitle as movie,
    sum(public.orderdetail.quantity) as moviesales
FROM
    public.orderdetail
    INNER JOIN public.orders ON public.orderdetail.orderid = public.orders.orderid
    INNER JOIN public.products ON public.products.prod_id = public.orderdetail.prod_id
    INNER JOIN public.imdb_movies ON public.imdb_movies.movieid = public.products.movieid
GROUP BY
    yeardate,
    movie;


-- Rank asigna el valor 1 a las entradas con mayor numero de ventas por año (partition)
CREATE VIEW SalesPerYearMax AS
SELECT
    yeardate,
    movie,
    moviesales,
    RANK() OVER (
        PARTITION BY yeardate
        ORDER BY
            moviesales DESC
    ) sales_rank
FROM
    SalesPerYear;

-- ordenamos la tabla por el numero de ventas descendentes
-- Escogemos las entradas con rank = 1 entre los años que queremos
RETURN QUERY (
    SELECT
        CAST(yeardate AS int),
        CAST(movie AS bpchar),
        moviesales
    FROM
        SalesPerYearMax
    WHERE
        sales_rank = 1 AND
        yeardate BETWEEN $1 AND $2
    ORDER BY
        moviesales DESC
);

DROP VIEW IF EXISTS SalesPerYear CASCADE;

END;

$$ LANGUAGE plpgsql;


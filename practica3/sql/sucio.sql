
SELECT *
FROM customers
INNER JOIN orders
ON orders.customerid = customers.customerid
WHERE creditcardtype = 'VISA'
AND orderdate = TO_DATE('201604', 'YYYYMM');



SELECT A. movieid, A.movietitle, A.year, A.ratingmean, A.ratingcount
FROM imdb_movies as A
INNER JOIN imdb_moviecountries as B
ON A.movieid=B.movieid
WHERE B.country = 'UK'
ORDER BY A.year DESC
LIMIT 400;

SELECT B.genre
FROM imdb_movies as A
INNER JOIN imdb_moviegenres as B
ON A.movieid=B.movieid
WHERE B.movieid='29955'

SELECT C.directorname
FROM imdb_movies as A 
INNER JOIN imdb_directormovies as B ON A.movieid=B.movieid
INNER JOIN imdb_directors as C ON B.directorid=C.directorid
WHERE B.movieid='29955'

SELECT movietitle, ratingmean
FROM imdb_movies 
WHERE movieid=44392;



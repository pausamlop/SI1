CREATE OR REPLACE 
FUNCTION setCustomersBalance(IN initialBalance bigint) 
RETURNS void as 
$$
UPDATE
    public.customers
SET
    balance = floor(initialBalance * random()) 
$$ LANGUAGE sql;


SELECT setCustomersBalance(100);


SELECT B.orderdate, E.movietitle, E.year, D.price
FROM public.customers AS A
        INNER JOIN public.orders AS B on A.customerid = B.customerid
        INNER JOIN public.orderdetail AS C on C.orderid = B.orderid
        INNER JOIN public.products as D on C.prod_id = D.prod_id
        INNER JOIN public.imdb_movies as E on E.movieid = D.movieid

    WHERE A.customerid = 158 and B.orderid=2208
    ORDER BY B.orderid;


SELECT orderid FROM orders WHERE customerid=158;

SELECT customerid FROM customers WHERE username='elena';

SELECT orderid FROM orders WHERE customerid= AND status is NULL

SELECT B.orderdate, E.movietitle, E.year, D.price
FROM public.orderdetail AS A on A.orderid = 5
        INNER JOIN public.products as B on B.prod_id = A.prod_id
        

    WHERE A.customerid = 158 and B.orderid=2208
    ORDER BY B.orderid;
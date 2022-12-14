-- Elena Cano Castillejo y Paula Samper Lopez
-- Archivo estadosDistintos.sql

-- numero de estados distintos de clientes con pedidos en un ano (ej 2017)
-- y que pertenecen a un country (ej Peru)

-- indice con el ano
CREATE INDEX index_orderdate 
ON public.orders(extract (year from orderdate));

-- indice con el pais
CREATE INDEX index_country
ON public.customers(country);

-- query con explain
EXPLAIN SELECT count(distinct C.state)
FROM public.customers as C
    INNER JOIN public.orders as O ON C.customerid = O.customerid
WHERE extract(year from O.orderdate) = 2017
    AND C.country = 'Peru';

-- drop INDEX index_orderdate;
-- drop INDEX index_country;


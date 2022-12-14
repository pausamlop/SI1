-- Creamos los carros con el status null

--Miramos cual ha sido el ultimo orderid para no liarla
INSERT INTO public.orders
VALUES (181791, ('2019-04-12')::date , 1, 100, 15, 115, NULL);

INSERT INTO public.orders
VALUES (181792, ('2017-03-09')::date , 2, 50, 15, 57.5 , NULL);

--Hacemos un update de la promo para ver si funciona el trigger
UPDATE public.customers
SET promo = 10
WHERE customerid = 1;

UPDATE public.orders
SET status = NULL
WHERE customerid = 1;
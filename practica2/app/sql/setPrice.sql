-- Elena Cano Castillejo y Paula Samper López
-- Archivo setPrice.sql


-- Actualizar price de orderdetail con price de products y con los años que han pasado desde la venta

UPDATE
    public.orderdetail
SET
    price = public.products.price - 0.02 *
        ( EXTRACT(YEAR FROM CURRENT_DATE ) - 
        EXTRACT(YEAR FROM public.orders.orderdate ))
FROM
    public.products,
    public.orders
WHERE
    public.orderdetail.prod_id = public.products.prod_id
    and public.orderdetail.orderid = public.orders.orderid;



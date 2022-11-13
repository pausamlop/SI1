-- Elena Cano Castillejo y Paula Samper López
-- Archivo setPrice.sql


-- Actualizar price de orderdetail con price de products

UPDATE
    public.orderdetail
SET
    price = public.products.price
FROM
    public.products 
WHERE 
	public.orderdetail.prod_id = public.products.prod_id;

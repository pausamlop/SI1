-- Elena Cano Castillejo y Paula Samper Lopez
-- Archivo updPromo.sql

-- Nueva columna promo en la tabla customers
ALTER TABLE
    public.customers
ADD 
    promo decimal(4,2);

-- inicializar el campo a 0 para operar
UPDATE
    public.customers
SET
    promo = 0;


---------------------------------TRIGGER---------------------------------------
CREATE
OR REPLACE FUNCTION updPromoTrigger() RETURNS TRIGGER AS $$ 


BEGIN

-- se actualiza el valor promo de un cliente
IF (TG_OP = 'UPDATE') THEN

    PERFORM pg_sleep(20);

    UPDATE orderdetail
    SET price = products.price * ((100-NEW.promo)/100)
    FROM products, customers, orders
    WHERE NEW.customerid = orders.customerid
        AND orders.orderid = orderdetail.orderid
        AND orders.status is NULL
        AND orderdetail.prod_id = products.prod_id;


    UPDATE public.orders
    SET 
        netamount = ((netamount*100)/(100-OLD.promo)) * ((100-NEW.promo)/100),
        totalamount = ((netamount*100)/(100-OLD.promo)) * ((100-NEW.promo)/100) * (1 + tax/100)
    WHERE NEW.customerid = customerid   
        AND status is NULL;


END IF;

RETURN NULL;

END;

$$ LANGUAGE plpgsql;


-- trigger
CREATE TRIGGER UpdatePromoTrigger AFTER
UPDATE
    ON customers FOR EACH ROW EXECUTE PROCEDURE updPromoTrigger();

---------------------------------------------------------------------------------------------------------

--Crear uno o varios carritos (status a NULL)
UPDATE public.orders
SET status = NULL
WHERE customerid = 1;
-- Elena Cano Castillejo y Paula Samper López
-- Archivo updOrders.sql


-- actualizar la tabla orders cuando se añada, actualice  elimine un elemento del carrito

-- funcion que ejecuta el trigger
CREATE
OR REPLACE FUNCTION updOrders() RETURNS TRIGGER AS $$ 


BEGIN


-- cambiar la fecha
UPDATE
    public.orders
SET
    orderdate = CURRENT_DATE;


-- se inserta un producto en el carrito (se añade un orderdetail)
IF (TG_OP = 'INSERT') THEN
    UPDATE
        public.orders
    SET
        -- net amount
        netamount = netamount + NEW.quantity * NEW.price,
        -- total amount
        totalamount = round ((netamount + NEW.quantity * NEW.price)* (1 + public.orders.tax/100), 2)
    WHERE 
        orderid = NEW.orderid;


-- se elimina un producto del carrito
ELSIF (TG_OP = 'DELETE') THEN
    UPDATE
        public.orders
    SET
        -- net amount
        netamount = netamount - OLD.quantity * OLD.price,
        -- total amount
        totalamount = round ((netamount - OLD.quantity * OLD.price)* (1 + public.orders.tax/100), 2)
    WHERE 
        orderid = OLD.orderid;


-- se actualiza la cantidad/precio de un producto del carrito
ELSIF (TG_OP = 'UPDATE') THEN
    UPDATE
        public.orders
    SET
        -- net amount
        netamount = netamount - OLD.quantity * OLD.price + NEW.quantity * NEW.price,
        -- total amount
        totalamount = round ((netamount - OLD.quantity * OLD.price + NEW.quantity * NEW.price) * (1 + public.orders.tax/100), 2)
    WHERE 
        orderid = NEW.orderid;


END IF;

RETURN NULL;

END;

$$ LANGUAGE plpgsql;



-- trigger
CREATE TRIGGER UO AFTER
INSERT OR DELETE OR UPDATE
    ON public.orderdetail FOR EACH ROW EXECUTE PROCEDURE updOrders();


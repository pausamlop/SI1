-- Elena Cano Castillejo y Paula Samper López
-- Archivo updInventoryAndCustomer.sql



-- actualizar la tabla 'inventory' y descontar en la tabla ‘customers’ el precio total de la compra

-- funcion que ejecuta el trigger
CREATE OR REPLACE FUNCTION updInventoryAndCustomer() RETURNS TRIGGER AS $$ 

BEGIN

-- el if no es necesario pero lo dejo por seguir la estructura de los demás triggers
IF (TG_OP = 'UPDATE') THEN

    -- se actualiza inventory
    UPDATE public.inventory
    SET 
        stock = C.stock - B.quantity,
        sales = C.sales + B.quantity


    FROM public.orders AS A
        INNER JOIN public.orderdetail AS B on A.orderid = B.orderid 
        INNER JOIN public.inventory AS C on C.prod_id = B.prod_id

    WHERE inventory.prod_id = B.prod_id and B.orderid = A.orderid;



    --se actualiza el customers
    UPDATE public.customers
    SET 
        balance = balance - NEW.totalamount
    FROM public.orders
    WHERE customers.customerid = NEW.customerid;



END IF;

RETURN NULL;

END;

$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS UIAC;

-- trigger para caundo un pedido pase al estado 'Paid' por lo que será solo para update
CREATE TRIGGER UIAC AFTER
UPDATE OF status
ON  public.orders FOR EACH ROW 
WHEN (OLD.status != 'Paid' and NEW.status = 'Paid')
EXECUTE PROCEDURE updInventoryAndCustomer();




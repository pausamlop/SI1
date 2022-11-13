-- Elena Cano Castillejo y Paula Samper López
-- Archivo setOrderAmount.sql

CREATE OR REPLACE PROCEDURE setOrderAmount()

LANGUAGE plpgsql AS
$$
BEGIN

-- actualizar net amount
UPDATE
    public.orders
SET
    netamount = order_netamount.netamount
FROM
    (
        SELECT
            orderid,
            sum(price * quantity) as netamount
        FROM
            public.orderdetail
        GROUP BY
            orderid
    ) as order_netamount
WHERE
    public.orders.orderid = order_netamount.orderid
    AND public.orders.netamount is NULL;

-- actualizar total amount
UPDATE
    public.orders
SET
    totalamount = round(orders.netamount + (orders.netamount * orders.tax / 100), 2)
WHERE
    public.orders.totalamount is NULL;


END
$$;




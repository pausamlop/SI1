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




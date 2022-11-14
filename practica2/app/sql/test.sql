CREATE
OR REPLACE FUNCTION setCustomersBalance(IN initialBalance bigint) RETURN void $$

BEGIN

UPDATE
    public.customers
SET
    balance = FLOOR(RAND()*initialBalance);
END;
$$ LANGUAGE plpgsql;

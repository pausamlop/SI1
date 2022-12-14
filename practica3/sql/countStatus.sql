-- query 1
-- explain select count(*)
-- from orders
-- where status is null;

-- query 2
-- explain select count(*)
-- from orders
-- where status = 'Shipped';

-- indice
-- CREATE INDEX index_status
-- ON public.orders(status);

-- estadisticas
-- ANALYZE public.orders;

-- query 3
-- explain select count(*)
-- from orders
-- where status ='Paid';

-- query 4
explain select count(*)
from orders
where status ='Processed';
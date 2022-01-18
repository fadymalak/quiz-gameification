CREATE OR REPLACE FUNCTION add_x(x text)
RETURNS int 
language plpgsql 
as 

$$
declare
datax integer ; 
begin
select country_name  from countries where 1 = 1 ;

end;
$$;

DROP PROCEDURE addxx;
CREATE OR REPLACE PROCEDURE addxx()
LANGUAGE plpgsql 
	as $$
declare 
data text;
BEGIN
select  count(*) into data from countries where 1= 1;
return ;
END ;
$$
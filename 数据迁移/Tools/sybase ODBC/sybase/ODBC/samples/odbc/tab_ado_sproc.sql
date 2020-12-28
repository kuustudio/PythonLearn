-- March 2003
-- Sybase, Inc 
-- test table for vb app
create table ado_table(c1 int, c2 char(20), c3 numeric(10,2), c4 datetime)
go

-- sp to insert data into table:
create proc sp_ado_insert (@id integer = 10) as
declare @a integer
declare @b numeric (10,2)
select @a = 1
select @b = 12345.67
while @a <= @id
begin
     insert into ado_table values (@a, 'xyz', @b, getdate())
     select @a = @a + 1
     select @b = @b + 789.02
end
go

-- Data in table:
-- c1    c2          c3          c4
----   -----       ----------  -------------------
-- 1     xyz         12345.67    Sep 23 1999  4:58PM
-- 2     xyz         13134.69    Sep 23 1999  4:58PM
-- 3     xyz         13923.71    Sep 23 1999  4:58PM
-- 4     xyz         14712.73    Sep 23 1999  4:58PM
-- 5     xyz         15501.75    Sep 23 1999  4:58PM
-- 6     xyz         16290.77    Sep 23 1999  4:58PM
-- 7     xyz         17079.79    Sep 23 1999  4:58PM
-- 8     xyz         17868.81    Sep 23 1999  4:58PM
-- 9     xyz         18657.83    Sep 23 1999  4:58PM
--10     xyz         19446.85    Sep 23 1999  4:58PM

-- sp to select all data:
create procedure sp_ado_table
as
select * from ado_table
go

-- sp to select row by column c1 (select c3, c4)
create procedure sp_ado_c3_c4 (@inp integer)
as
select c3, c4 from ado_table where c1=@inp
go

-- sp to select row by column c1, c2 (select c3, c4)
create procedure sp_ado_2parm (@inp integer, @inp2 char(20))
as
select c3, c4 from ado_table where c1=@inp and c2 = @inp2
return 88
go

-- use output parm
create procedure sp_ado_out_c3_c4 (@out integer output)
as
select c3, c4 from ado_table where c1=@out
select @out=200

go

--- datetime output
create procedure sp_ado_outdate_c3_c4 (@out datetime output)
as
select c3, c4 from ado_table where c4=@out
select @out=getdate()

go

--- numeric output
create procedure sp_ado_outnum_c3_c4 (@out numeric(10,2) output)
as
select c3, c4 from ado_table where c3=@out
select @out = @out + 12.34
go

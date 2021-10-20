-- 1. Инструкция SELECT, использующая предикат сравнения.
select distinct t.root_number, t.transport_type
from transport t join transport as t2 on t.transport_type = t2.transport_type
where t2.start_id != t.start_id and t.entry_date = '1982-08-24'
order by t.root_number, t.transport_type;

-- 2. Инструкция SELECT, использующая предикат BETWEEN.
select distinct name, address
from transport_stop
where install_year between '1997-01-01' and '1997-03-31';

-- 3. Инструкция SELECT, использующая предикат LIKE.
select distinct root_number, start_id, stop_id
from fare
where day_time like 'с 9%';

-- 4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом.
select root_number, start_id, stop_id
from fare
where root_number in
(
	select root_number
	from transport
	where transport_type = 'автобус'
) and price > 50;

-- 5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом.
select root, timing
from timetable
where exists
(
	select *
	from transport_stop
	where install_year > '1990-02-23'
);

-- 6. Инструкция SELECT, использующая предикат сравнения с квантором
select root, max_price
from timetable
where max_price > all
(
	select max_price
	from fare
	where start_id = 123
);

-- 7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов.
select avg(price)
from fare
group by start_id;

-- 8. Инструкция  SELECT, использующая скалярные подзапросы в выражениях столбцов.
select
(
	select name
	from transport_stop limit 1
);

-- 10. Инструкция SELECT, использующая поисковое выражение CASE.
select root,
case
	when weekends = true then
		'work'
	when weekends = false then
		'not work'
end weekends
from timetable;

-- 16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной строки значений.
insert into transport values (1, 78, 53, 'троллейбус', '1882-08-24');

-- 17. Многострочная инструкция INSERT, выполняющая вставку в таблицу результирующего набора данных вложенного подзапроса.
insert into transport
select
(
	select max(root)
	from timetable
	where max_price = 121
), start_id, stop_id, 'маршрутка', '2001-07-06'
from transport;

-- 18. Простая инструкция UPDATE.
update timetable
set timing = timing + '00:15:00'
where transport_stop_id = 956;

-- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET.
update timetable
set max_price =
(
	select avg(price)
	from fare
	where root_number = 12
)
where root = 12;

-- 20. Простая инструкция DELETE.
delete from transport_stop
where install_year = '1999-02-19';

-- 23. Инструкция  SELECT, использующая рекурсивное обобщенное табличное выражение. 
with recursive cte as
(
	select '09:00:00' as timing, transport_stop_id, root, weekends, max_price
	from timetable
	union all
	select timing + '00:30:00', transport_stop_id, root, weekends, max_price
	from timetable
	where timing <= '21:00:00' and timing >= '09:00:00'
)

select *
from cte
order by timing;

-- 25. Оконные функции для устранения дублей 
select t.root, t.transport_stop_id
into temp temp_table
from timetable as t join fare as f on t.root = f.root_number;

delete from temp_table
where root in
(
	select root from
	(
		select *, row_number() over (partition by root, transport_stop_id) as unique_val
		from temp_table
	) as tt
	where tt.unique_val > 1
);

-- Защита: вывести кол-во остановок со всеми видами транспорта
select count(*)
from transport as t join transport_stop as ts on (ts.id = t.start_id or ts.id = t.stop_id) and ts.electricity is true and ts.rails is true;
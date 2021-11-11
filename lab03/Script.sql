-- Скалярная функция
create or replace function time_diff(x time) returns time language sql as
$$
	select x -
	(
		select avg(timing)
		from timetable
	)
$$;

select time_diff(timing) as difference
from timetable
where weekends is false;

-- Подставляемая табличная функция или многооператорная табличная функция (?)
create or replace function fulltable() returns table(root_number int, timing time, max_price numeric) language sql as
$$
	select root_number, timing, max_price
	from transport as t join timetable as tt on t.stop_id = tt.transport_stop_id
$$;

select *
from fulltable();

-- Рекурсивная функция или функция с рекурсивным ОТВ
create or replace function rec() returns table(timing time, transport_stop_id int, root int, weekends bool, max_price numeric) language sql as
$$
	with recursive cte2(timing, transport_stop_id, root, weekends, max_price) as
	(
		select '09:00:00'::time as timing, transport_stop_id, root, weekends, max_price
		from timetable
		union
		select t.timing + '00:30:00', t.transport_stop_id, t.root, t.weekends, t.max_price
		from timetable t join cte2 c on t.transport_stop_id = c.transport_stop_id
		where t.timing <= '11:00:00' and t.timing >= '09:00:00'
	)

	select *
	from cte2
	order by timing;
$$;

select *
from rec();

-- Хранимая процедура без параметров или с параметрами
create or replace procedure insert_transport_data(root_number int, start_id int, stop_id int, transport_type text, entry_date date) language plpgsql as
$$ begin
	if root_number = 0 or start_id = 0 or stop_id = 0 then
		raise notice 'Проверьте аргументы функции';
	else
		insert into transport values (root_number, start_id, stop_id, transport_type, entry_date);
	end if;
end $$;

call insert_transport_data(0, 78, 53, 'троллейбус', '1882-08-24');

-- Рекурсивная хранимая процедура или хранимая процедура с рекурсивным ОТВ
create or replace procedure shift_request(call_count int, max_count int) language plpgsql as
$$ begin
	if call_count < max_count then
		call shift_request(call_count + 1, max_count);
	end if;

	update transport_stop
	set request_stop = not request_stop;
end $$;

call shift_request(1, 10);

-- Хранимая процедура с курсором
create or replace procedure renovation(bus_entry_date date) language plpgsql as
$$
declare
	row record;
	cur cursor for
		select *
		from transport
		where entry_date < bus_entry_date;
begin
	open cur;
	loop
		fetch cur into row;
		exit when not found;

		update transport_stop
		set rails = true;
	end loop;
	close cur;
end $$;

call renovation('1950-01-01');

-- Хранимая процедура доступа к метаданным
select *
from information_schema.table_constraints;

create or replace procedure show_all_PK() language plpgsql as
$$
declare
	cur cursor for
		select constraint_name, table_name, constraint_type
		from information_schema.table_constraints
		where constraint_type = 'PRIMARY KEY';
	row record;
begin
	open cur;
	loop
		fetch cur into row;
		exit when not found;
		raise notice 'Constraint: % in table: %', row.constraint_name, row.table_name;
	end loop;
	close cur;
end $$;

call show_all_PK();

-- Триггер AFTER
create temp table temp_fare
(
	root_number int not null,
	price numeric not null,
	at_day bool not null,
	num_after_this int not null
);

create or replace function inc_num() returns trigger language plpgsql as
$$ begin
	update temp_fare
	set num_after_this = num_after_this + 1;
	return new;
end $$;

create trigger trigger_after_insert
after insert on temp_fare for each row
execute function inc_num();

insert into temp_fare values (1, 15, true, -1);
insert into temp_fare values (2, 20, true, -1);
insert into temp_fare values (3, 30, false, -1);
insert into temp_fare values (4, 10, true, -1);
insert into temp_fare values (5, 15, false, -1);

select *
from temp_fare order by num_after_this;

-- Триггер INSTEAD OF
create view transport_view as
select *
from transport;

create or replace function cancel_update() returns trigger language plpgsql as
$$ begin
	raise notice 'permission denied';
	return new;
end $$;

create trigger cancel_update_trigger
instead of update on transport_view for each row
execute function cancel_update();

update transport_view
set transport_type = 'троллейбус'
where root_number = 1;

-- по названию остановки вывести все номера маршрутов
create or replace function show_root_numbers(naming text) returns int language sql as
$$
	select t.root_number
	from transport t join transport_stop ts on ts.id = t.start_id or ts.id = t.stop_id
	where ts.name = naming;
$$;

select *
from show_root_numbers('наб. Тракторная, д. 149 стр. 419');
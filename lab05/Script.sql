-- 1. Из таблиц базы данных, созданной в первой лабораторной работе, извлечь данные в  XML  (MSSQL) или  JSON(Oracle,  Postgres).
-- Для выгрузки в  XML проверить все режимы конструкции FOR XML
copy
(
	select row_to_json(fare)
	from fare
)
to 'D:\bd\lab05\fare.json';

-- 2. Выполнить загрузку и сохранение XML или JSON файла в таблицу.
-- Созданная таблица после всех манипуляций должна соответствовать таблице базы данных, созданной в первой лабораторной работе.
create table temp_fare(row json);
copy temp_fare from 'D:\bd\lab05\fare.json';

select x.root_number, x.price, x.start_id, x.stop_id, x.day_time
into json_fare
from temp_fare as tf, json_to_record(tf.row)
as x(root_number int, price numeric, start_id int, stop_id int, day_time text);

select *
from fare;
select *
from json_fare;

-- Создать таблицу, в которой будет атрибут(-ы) с типом XML или JSON, или добавить атрибут с типом  XML или  JSON к уже существующей таблице.
-- Заполнить атрибут правдоподобными данными с помощью команд  INSERT или UPDATE.
create table if not exists json_transport
(
	root_number int,
	start_id int,
	stop_id int,
	transport_type text,
	entry_date json
);

insert into json_transport (root_number, start_id, stop_id, transport_type, entry_date)
select root_number, start_id, stop_id, transport_type, json_build_object
	(
		'day', extract(day from entry_date),
		'month', extract(month from entry_date),
		'year', extract(year from entry_date)
	)
from transport;

select *
from json_transport;

-- 4. Выполнить следующие действия:
-- 4.1. Извлечь  XML/JSON фрагмент из XML/JSON документа
select *
from temp_fare limit 1;

-- 4.2. Извлечь значения конкретных узлов или атрибутов XML/JSON документа
select row->>'root_number' as root_number, row->>'price' as price
from temp_fare
where row->>'day_time' = 'с 0 до 9';

-- 4.3. Выполнить проверку существования узла или атрибута
select row, row::jsonb? 'start_id' as start_id_exists, row::jsonb? 'stop_id' as stop_id_exists
from temp_fare;

-- 4.4. Изменить XML/JSON документ
update temp_fare
set row = jsonb_set(row::jsonb, '{day_time}', '"c 6 до 12"'::jsonb, false)
where row->>'day_time' = 'с 2 до 3';

--4.5. Разделить XML/JSON документ на несколько строк по узлам
copy
(
	select *
	from temp_fare
	where (row->>'price')::numeric > 5
)
to 'D:\bd\lab05\faremorefive.json';

select x.root_number, x.price, x.start_id, x.stop_id, x.day_time
into json_fare
from temp_fare as tf, json_to_record(tf.row)
as x(root_number int, price numeric, start_id int, stop_id int, day_time text);

select json_build_object
	(
		'root_number', root_number,
		'start_id', start_id,
		'stop_id', stop_id
	) as identies,
	jsonb_build_object
	(
		'price', price,
		'day_time', day_time
	) as descripties
from temp_fare as tf, json_to_record(tf.row)
as x(root_number int, price numeric, start_id int, stop_id int, day_time text);

-- удалить из таблицы два каких-нибудь атрибута
update temp_fare
set row = row::jsonb - 'price'::text - 'day_time'::text
where (row->>'stop_id')::int > 900;

select *
from temp_fare
where (row->>'stop_id')::int > 889;
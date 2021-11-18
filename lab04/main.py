import psycopg2
from psycopg2 import Error

def scalar_function(cursor):
	cursor.execute(
		'''
		create or replace function time_diff(x time) returns time language sql as
			$$
				select x -
				(
					select avg(timing)
					from timetable
				)
			$$;
		'''
	)
	# Получить результат
	connection.commit()
	print('Скалярная функция успешно создана.')

	cursor.execute(
		'''
			select time_diff(timing) as difference
			from timetable
			where weekends is false;
		'''
	)
	print('  difference   |\n---------------+')
	time = cursor.fetchall()
	for i in range(200):
		print(time[i][0], end = '|\n')

def aggregate(cursor):
	cursor.execute(
		'''
			create aggregate sum(numeric)
			(
				sfunc = numeric_add,
				stype = numeric,
				initcond = '0'
			);
		'''
	)
	connection.commit()
	print('Агрегатная функция успешно создана.')

	cursor.execute(
		'''
			select sum(price)
			from fare;
		'''
	)
	print('  sum   |\n--------+')
	result = cursor.fetchone()
	print(result[0])

def table_function(cursor):
	cursor.execute(
		'''
			create or replace function fulltable() returns table(root_number int, timing time, max_price numeric) language sql as
			$$
				select root_number, timing, max_price
				from transport as t join timetable as tt on t.stop_id = tt.transport_stop_id
			$$;
		'''
	)
	connection.commit()
	print('Табличная функция успешно создана.')

	cursor.execute(
		'''
			select *
			from fulltable();
		'''
	)
	result = cursor.fetchall()
	print('root_number|timing  |max_price          \n|-----------+--------+-------------------+')
	for i in range(200):
		print(result[i][0], result[i][1], result[i][2], sep = '|')

def procedure(cursor):
	cursor.execute(
		'''
			create or replace procedure insert_transport_data(root_number int, start_id int, stop_id int, transport_type text, entry_date date) language plpgsql as
			$$ begin
				if root_number = 0 or start_id = 0 or stop_id = 0 then
					raise notice 'Проверьте аргументы функции';
				else
					insert into transport values (root_number, start_id, stop_id, transport_type, entry_date);
				end if;
			end $$;
		'''
	)
	connection.commit()
	print('Хранимая процедура успешно создана.')

	cursor.execute(
		'''
			call insert_transport_data(0, 78, 53, 'троллейбус', '1882-08-24');
		'''
	)
	result = cursor.fetchone()
	# print('root_number|timing  |max_price          \n|-----------+--------+-------------------+')
	# for i in range(200):
	# 	print(result[i][0], result[i][1], result[i][2], sep = '|')

def trigger(cursor):
	cursor.execute(
		'''
			create temp table temp_fare
			(
				root_number int not null,
				price numeric not null,
				at_day bool not null,
				num_after_this int not null
			);
		'''
	)
	connection.commit()
	print('Временная таблица успешно создана.')

	cursor.execute(
		'''
			create or replace function inc_num() returns trigger language plpgsql as
			$$ begin
				update temp_fare
				set num_after_this = num_after_this + 1;
				return new;
			end $$;
		'''
	)
	connection.commit()
	print('Функция для триггера успешно создана.')

	cursor.execute(
		'''
			create trigger trigger_after_insert
			after insert on temp_fare for each row
			execute function inc_num();
		'''
	)
	connection.commit()
	print('Триггер успешно создан.')
	cursor.execute(
		'''
			insert into temp_fare values (1, 15, true, -1);
		'''
	)
	connection.commit()
	cursor.execute(
		'''
			insert into temp_fare values (2, 20, true, -1);
		'''
	)
	connection.commit()
	cursor.execute(
		'''
			insert into temp_fare values (3, 30, false, -1);
		'''
	)
	connection.commit()
	cursor.execute(
		'''
			insert into temp_fare values (4, 10, true, -1);
		'''
	)
	connection.commit()
	cursor.execute(
		'''
			insert into temp_fare values (5, 15, false, -1);
		'''
	)
	connection.commit()
	cursor.execute(
		'''
			select *
			from temp_fare order by num_after_this;
		'''
	)

	result = cursor.fetchall()
	print('root_number|price|at_day|num_after_this|\n-----------+-----+------+--------------+')
	for i in range(5):
		print(result[i][0], result[i][1], result[i][2], result[i][3], sep = '|')

def user_type(cursor):
	cursor.execute(
		'''
		create type transp_info as
		(
			id int,
			name text
		);
		'''
	)
	connection.commit()
	cursor.execute(
		'''
			create or replace function get_trans_info() returns transp_info language sql as
			$$
					select id, name
					from transport_stop;
			$$;
		'''
	)
	print('Функция для вывожа данных успешно создана.')
	connection.commit();
	cursor.execute(
		'''
			select *
			from get_trans_info();
		'''
	)

	result = cursor.fetchall()
	for i in range(200):
		print(result)

# Защита как в третьей лабе
def protection(cursor):
	cursor.execute(
		'''
			create or replace function show_root_numbers(naming text) returns int language sql as
			$$
				select t.root_number
					from transport t join transport_stop ts on ts.id = t.start_id or ts.id = t.stop_id
					where ts.name = naming;
				$$;
			'''
		)
	connection.commit()
	print('Функция успешно создана.')

	cursor.execute(
		'''
			select *
			from show_root_numbers('наб. Тракторная, д. 149 стр. 419');
		'''
	)
	result = cursor.fetchall()
	print('show_root_numbers|\n-----------------+')
	for i in range(len(result)):
		print(result[i][0], end = '|\n')

try:
	# Подключение к существующей базе данных
	connection = psycopg2.connect(user = "postgres", password = "", host = "127.0.0.1", port = "5432", database = "postgres")

	# Курсор для выполнения операций с базой данных
	cursor = connection.cursor()
	# Выполнение SQL-запроса
	scalar_function(cursor)
	print()
	aggregate(cursor)
	print()
	table_function(cursor)
	print()
	procedure(cursor)
	print()
	trigger(cursor)
	print()
	user_type(cursor)
	print()
	protection(cursor)

except (Exception, Error) as error:
	print("Ошибка при работе с PostgreSQL", error)
finally:
	if connection:
		cursor.close()
		connection.close()
		print("Соединение с PostgreSQL закрыто")
import psycopg2 as ps2
from psycopg2 import sql
from prettytable import PrettyTable

def scalar_query(cursor):
	print('\nНазвание и адрес остановок, которые были установлены с 1 января по 31 марта 1997 года')
	query = sql.SQL('select distinct name, address from transport_stop where install_year between \'1997-01-01\' and \'1997-03-31\';')
	cursor.execute(query)
	result = cursor.fetchall()
	table = PrettyTable(['Название', 'Адрес'])
	table.add_rows(result)
	print(table, '\n')

def join(cursor):
	print('\nКоличество остановок со всеми видами транспорта')
	query = sql.SQL('select count(*) from transport as t join transport_stop as ts on (ts.id = t.start_id or ts.id = t.stop_id) and ts.electricity is true and ts.rails is true;')
	cursor.execute(query)
	result = cursor.fetchall()
	table = PrettyTable(['Количество остановок'])
	table.add_row(result)
	print(table, '\n')

def metadata_query(cursor):
	print('\nНазвание ограничения и название таблицы, где тип ограничения - первичный ключ.')
	get_pk_constraints = sql.SQL('select constraint_name, table_name from information_schema.table_constraints where constraint_type = \'PRIMARY KEY\';')
	cursor.execute(get_pk_constraints)
	if cursor.rowcount > 0:
		result = cursor.fetchall()
	table = PrettyTable(['Название ограничения', 'Название таблицы'])
	table.add_rows(result)
	print(table, '\n')

def call_scalar_func(cursor):
	print('Разница между текущим и среднем временем на маршрутах, которые не работают по выходным')
	query = sql.SQL('select time_diff(timing) as difference from timetable where weekends is false;')
	cursor.execute(query)
	result = cursor.fetchone()
	table = PrettyTable(['Время'])
	table.add_rows(result)
	print(table, '\n')

def call_table_func(cursor):
	print('Номер маршрута, время, максимальная цена.')
	query = sql.SQL('select * from fulltable();')
	cursor.execute(query)
	result = cursor.fetchall()
	table = PrettyTable(['Номер маршрута', 'Время', 'Максимальная цена'])
	table.add_rows(result)
	print(table, '\n')

def stored_proc(cursor):
	print('Прибавление всем маршрутам между 9 и 11 часами 30 минут ко времени прибытия')
	query = sql.SQL('select * from rec();')
	cursor.execute(query)
	result = cursor.fetchall()
	table = PrettyTable(['Время', 'ID конечной остановки', 'Номер маршрута', 'Работает по выходным?', 'Максимальная цена'])
	table.add_rows(result)
	print(table, '\n')

def call_sys_func(cursor):
	print('\nПолучение информации о версии PosgreSQL.')
	cursor.callproc('version')
	result = cursor.fetchone()
	table = PrettyTable(['Версия PostgreSQL'])
	table.add_row(result)
	print(table, '\n')

def create_table(cursor):
	print('\nСоздание таблицы')
	cursor.execute('create table if not exists ticket (number serial not null primary key, company_name text, root_number int not null references transport(root_number), start_id int not null references transport_stop(id), stop_id int not null references transport_stop(id), timing time not null);')
	print(cursor.statusmessage)
	connection.commit()

def insert_table(cursor):
	print('\nСоздание таблицы')
	cursor.execute('insert into ticket(company_name, root_number, start_id, stop_id, timing) values (\'ааа\', 12, 34, 55, \'11:00:00\'::time), (\'бб\', 11, 54, 95, \'12:00:00\'::time), (\'ккк\', 636, 879, 111, \'11:30:00\'::time), (\'ггг\', 712, 234, 755, \'15:15:00\'::time);')
	print(cursor.statusmessage)
	connection.commit()

def defence(cursor):
	print('Вызов рекурсивной функции (макс. уровень 10). Обращение значения "остановка по требованию"')
	cursor.execute('call shift_request(1, 10);')
	print(cursor.statusmessage)
	connection.commit()

menu = '0. Завершить программу.\n' \
	'1. Выполнить скалярный запрос.\n' \
	'2. Выполнить запрос с несколькими соединениями (JOIN).\n' \
	'3. Выполнить запрос с ОТВ(CTE) и оконными функциями.\n' \
	'4. Выполнить запрос к метаданным.\n' \
	'5. Вызвать скалярную функцию (написанную в третьей лабораторной работе)\n' \
	'6. Вызвать многооператорную или табличную функцию (написанную в третьей лабораторной работе)\n' \
	'7. Вызвать хранимую процедуру (написанную в третьей лабораторной работе).\n' \
	'8. Вызвать системную функцию или процедуру;\n' \
	'9. Создать таблицу в базе данных, соответствующую тематике БД.\n' \
	'10. Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT или COPY.\n' \
	'11. Выполнить защиту\n' \
	'Выбранный пункт меню: '

connection = ps2.connect(user = 'postgres', password = 'pgadminkoro', host = '127.0.0.1', port = '5432', database = 'postgres')
cursor = connection.cursor()
queries = [exit, scalar_query, join, None, metadata_query, call_scalar_func, call_table_func, stored_proc, call_sys_func, create_table, insert_table, defence]

while 1:
	choose = int(input(menu))
	try:
		queries[choose](cursor)
	except:
		print('\nПункта с номером ' + choose + ' нет. Повторите ввод.')
connection.close()
from faker import Faker
from random import randint
import csv

fake = Faker('ru_RU')

def create_stops():
	with open('transport stops.csv', 'w', newline = '', encoding = 'utf8') as file:
		file.write('id,name,address,request_stop,install_year,electricity,rails\n')
		rows = []
		for i in range(900):
			a = fake.street_address()
			# id, name, address, request_stop, install_year, electricity, rails
			rows.append([i + 1, a, a, fake.boolean(), fake.date(), fake.boolean(), fake.boolean()])

		writer = csv.writer(file)
		writer.writerows(rows)

def create_transport():
	with open('transport.csv', 'w', newline = '', encoding = 'utf8') as file:
		file.write('root_number,start_id,stop_id,transport_type,entry_date\n')
		rows = []
		for _ in range(900):
			# root_number, start_id, stop_id, transport_type, entry_date
			rows.append([fake.unique.random_int(1, 998), fake.random_int(1, 998), fake.random_int(1, 998),
									fake.random_element(elements = ('трамвай', 'троллейбус', 'автобус', 'маршрутка', 'электробус')), fake.date()])

		writer = csv.writer(file)
		writer.writerows(rows)

def create_fare():
	with open('fare.csv', 'w', newline = '', encoding = 'utf8') as file:
		file.write('price,root_number,start_id,stop_id,day_time\n')
		rows = []
		for _ in range(900):
			# price, root_number, start_id, stop_id, day_time
			rows.append([float(fake.numerify(text = '##.##')), fake.random_int(1, 998), fake.random_int(1, 998), fake.random_int(1, 998),
									fake.numerify(text = 'с # до #')])

		writer = csv.writer(file)
		writer.writerows(rows)

def create_timetable():
	with open('timetable.csv', 'w', newline = '', encoding = 'utf8') as file:
		file.write('timing,transport_stop_id,root,weekends,max_price\n')
		rows = []
		for _ in range(900):
			# timing, transport_stop_id, root, weekends, max_price
			rows.append([fake.time(), fake.random_int(1, 998), fake.random_int(1, 998), fake.boolean(), float(fake.numerify(text = '##.##'))])

		writer = csv.writer(file)
		writer.writerows(rows)

create_stops()
create_transport()
create_fare()
create_timetable()
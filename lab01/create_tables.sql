create table if not exists timetable
(
	timing time null,
	transport_stop_id int4 null,
	root int4 null,
	weekends bool null,
	max_price money null,
	constraint timetable_pkey primary key (timing)
);

create table if not exists transport
(
	root_number int4 not null,
	start_id int4 not null,
	stop_id int4 null,
	transport_type text null,
	entry_date date null,
	constraint transport_pkey primary key (root_number)
);

create table if not exists transport_stop
(
	id serial null,
	name text null,
	address text null,
	request_stop bool null,
	install_year date null,
	constraint transport_stop_pkey primary key (id)
);

create table if not exists fare
(
	root_number int4 null,
	price money not null,
	start_id int4 not null,
	stop_id int4 not null,
	day_time text null,
	constraint fare_pkey primary key (price)
);

alter table transport_stop add electricity bool;
alter table transport_stop add rails bool;
alter table timetable add constraint timetable_max_price_fkey foreign key (max_price) references fare(price);
alter table timetable add constraint timetable_root_fkey foreign key (root) references transport(root_number);
alter table timetable add constraint timetable_transport_stop_id_fkey foreign key (transport_stop_id) references transport_stop(id);

alter table transport add constraint transport_start_id_fkey foreign key (start_id) references transport_stop(id);
alter table transport add constraint transport_stop_id_fkey foreign key (stop_id) references transport_stop(id);

alter table fare add constraint fare_root_number_fkey foreign key (root_number) references transport(root_number);
alter table fare add constraint fare_start_id_fkey foreign key (start_id) references transport_stop(id);
alter table fare add constraint fare_stop_id_fkey foreign key (stop_id) references transport_stop(id);
alter table transport_stop add constraint id_unique unique (id);

-- ???, ????, ???????? ?????

create trigger transport_stop_electricity
after insert on transport_stop
when (transport.transport_type = 'ענמככויבףס')
execute execute procedure --electricity = true

create trigger transport_stop_rails
after insert on transport_stop
when (transport.transport_type = 'ענאלגאי')
execute rails = true
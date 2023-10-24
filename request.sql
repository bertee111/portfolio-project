select * from user
select * from event
select * from enrollment
.schema
.tables

select e.user_id, e.title, e.date, er.user_id, u.email
from event e 
left join enrollment er on e.id = er.event_id
join user u on e.user_id = u.id

select e.user_id, date, u.name, count(er.user_id) 
from enrolment er 
join event e on e.user_id = er.user_id
join user u on u.user_id = e.user_id
where er.user_id = 2
group by e.uer_id, date

insert into enrollment (user_id, event_id, date) values (2,3,'2023-10-23');
insert into enrollment (user_id, event_id, date) values (2,6,'2023-10-23');
insert into event (user_id, title, date) values (3,'patate4','2023-10-23');

delete from event where id = 4
delete from enrollment where id = 10


PRAGMA foreign_keys=1;
insert into enrollment (user_id, event_id, date) values (2,14,'2023-10-23');


select e.id, e.title, e.date, u.id, u.username as owner, er.user_id as enroler, uer.username
from event e 
left join user u on e.user_id = u.id
left join enrollment er on e.id = er.event_id
left join user uer on er.user_id = uer.id


insert into event (user_id, title, date) values (2,'boxe','2023-10-23');
insert into event (user_id, title, date) values (2,'karate','2023-10-23');
insert into event (user_id, title, date) values (2,'judo','2023-10-23');
insert into event (user_id, title, date) values (2,'kendo','2023-10-23');
insert into event (user_id, title, date) values (3,'rock','2023-10-23');
insert into event (user_id, title, date) values (3,'disco','2023-10-23');
insert into event (user_id, title, date) values (3,'techno','2023-10-23');
insert into event (user_id, title, date) values (3,'classical','2023-10-23');

insert into enrollment (user_id, event_id, date) values (1,5,'2023-10-23');
insert into enrollment (user_id, event_id, date) values (2,5,'2023-10-23');
insert into enrollment (user_id, event_id, date) values (3,5,'2023-10-23');
insert into enrollment (user_id, event_id, date) values (1,10,'2023-10-23');
insert into enrollment (user_id, event_id, date) values (2,10,'2023-10-23');
insert into enrollment (user_id, event_id, date) values (3,10,'2023-10-23');





SELECT
    e.id AS event_id,
    e.title AS event_title,
    e.date AS event_date,
    u.id AS owner_id,
    u.username AS event_owner,
    er.user_id AS enrollee_id,
    uer.username AS enrollee_username
FROM
    event e
LEFT JOIN user u ON e.user_id = u.id
LEFT JOIN enrollment er ON e.id = er.event_id
LEFT JOIN user uer ON er.user_id = uer.id
ORDER BY event_id, enrollee_id;
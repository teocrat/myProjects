drop database if exists office_equipment_store;

create database  office_equipment_store character set utf8 collate utf8_general_ci;

use office_equipment_store;

drop table if exists users;

create table users 
   (id serial primary key,
   firstname varchar(50),
   lastname varchar(50),
   birthday date,
   phone bigint unique, 
   email varchar(100) unique,
   created_at date, 
   updated_at date,
   
  index user_firstname_lastname_idx(firstname, lastname)
);
 
 drop table if exists catalogs;

create table catalogs
   (id serial primary key,
   name varchar(255),
   
   index catalogs_name_idx(name)
);
  
 drop table if exists products;
   
 create table products
   (id serial primary key,
   name varchar(50),
   description varchar(255),
   price decimal(10, 2),
   catalogs_id bigint unsigned,
   created_at datetime default now(),
   updated_at  datetime default now() ON UPDATE now(),
   
   index products_name_idx(name),
   
   foreign key (catalogs_id) references catalogs(id)
   on delete cascade
   on update cascade
 );


drop table if exists discounts;

create table discounts
   (id serial primary key,
   products_id bigint unsigned,
   catalogs_id bigint unsigned,
   discount float,
   started_at date,
   finish_at date,
   created_at datetime default now(),
   updated_at datetime default now() on update now(),
   
   foreign key (products_id) references products(id)
   on delete cascade
   on update cascade,
   
   foreign key (catalogs_id) references catalogs(id)
   on delete cascade
   on update cascade
);

drop table if exists orders;

create table orders
   (id serial primary key,
   user_id bigint unsigned,
   created_at datetime default now(),
   updated_at datetime default now() on update now(),
   
   index orders_id_idx(id),
   
   foreign key (user_id) references users(id)
   on delete cascade
   on update cascade
 );

drop table if exists orders_products;

create table orders_products
   (id serial,
   orders_id bigint unsigned,
   products_id bigint unsigned,
   primary key (id,orders_id),
   amount int unsigned,
   created_at datetime default now(),
   updated_at datetime default now() on update now(),
   
   foreign key (orders_id) references orders(id)
   on delete cascade
   on update cascade,
   
   foreign key (products_id) references products(id)
   on delete cascade
   on update cascade 
);

drop table if exists warehouse;

create table warehouse
   (id serial primary key,
   name varchar(255),
   created_at datetime default now(),
   updated_at datetime default now() on update now(),
   
   index warehouse_name_idx(name)
);

drop table if exists warehouse_products;


create table warehouse_products
   (id serial primary key,
   warehouse_id bigint unsigned,
   products_id bigint unsigned,
   amount bigint,
   created_at datetime default now(),
   updated_at datetime default now() on update now(),
     
   foreign key (warehouse_id) references warehouse(id)
   on delete cascade
   on update cascade,
   
   foreign key (products_id) references products(id)
   on delete cascade
   on update cascade   
);

drop table if exists favorits;

create table favorits
  (id serial primary key,
  users_id bigint unsigned,
  products_id bigint unsigned,
  created_at datetime default now(),
  updated_at datetime default now() on update now(),
   
   foreign key (users_id) references users(id)
   on delete cascade
   on update cascade,
   
   foreign key (products_id) references products(id)
   on delete cascade
   on update cascade 
);

drop table if exists delivery;

create table delivery
   (id serial primary key,
   orders_id bigint unsigned,
   address varchar(255),
   created_at datetime,
   finish_at datetime,
   
   foreign key (orders_id) references orders(id)
   on delete cascade
   on update cascade 
);

drop table if exists brends;

create table brends
   (id serial primary key,
   name varchar(50),
   
   index brends_name_idx(name)
);

drop table if exists selection_by_brands;

create table selection_by_brends
   (id serial primary key,
   brends_id  bigint unsigned,
   products_id bigint  unsigned,
   
   
   foreign key (brends_id) references brends(id)
   on delete cascade
   on update cascade,
   
   foreign key (products_id) references products(id)
   on delete cascade
   on update cascade   
);



   
   
   








 
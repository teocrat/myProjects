use office_equipment_store;

-- выборка средней цены по магазину по каталогу
select name,
	   (select round(avg(price),2)  from products
	    where  catalogs_id = catalogs.id) as avg_price
from catalogs
group by name;

-- выборка невыполненых заказов(доставок)

select orders_id as 'Outstanding orders',
	   address
from delivery 
where finish_at >= now()
group by orders_id;

-- выборка продукции на которую распространяется скидка

select (select name from products
	   where id = discounts.products_id) as product,	   
	   discount
from discounts;

-- выборка количества товара на складах

select w.name, 
	   sum(wp.amount) as amount
from warehouse w 
join warehouse_products wp 
on w.id = wp.warehouse_id 
group by name;
		
-- выборка избранного по пользователям

select p.name as item_name,
       concat(u.firstname,' ',u.lastname) as user_name	   
from users u 
join products p 
join favorits f 
on u.id = f.users_id 
and p.id = f.products_id 
order by user_name;

-- выборка самого популярного товара 

select p.name as most_popular_item,
	   sum(amount) as amount_orders
from products p 
join orders_products op 
on p.id = op.products_id
group by most_popular_item
order by amount_orders desc 
limit 1;



-- представление соответсвия единиц продукции названиям в каталоге

create or replace view prod(product, category)
as select p.name, c.name 
from products p
join catalogs c 
on p.catalogs_id = c.id
;


-- представление доставки по заказу и заказчику

create or replace view deliveries(
						order_number,
						product,
						amount,
						customer,
						address,
						`date_order`)
						
              as select op.orders_id,
             			p.name,
             			op.amount,
             			concat(u.firstname, ' ',u.lastname),
             			d.address,
             			d.created_at
              from orders_products op 
              join products p 
              join users u 
              join delivery d 
              join orders o 
              on op.orders_id = d.orders_id
              and op.products_id = p.id
              and u.id = o.user_id
              and o.id = op.orders_id 
              group by op.orders_id
              order by op.orders_id;
             
             
             
 -- триггер предупреждения отсутствия адреса в таблице доставки
             
drop trigger if exists check_address_delivery;

delimiter //

create trigger check_address_delivery
before insert on delivery
for each row
begin
	if new.address is null
	then signal sqlstate '45000'
	set message_text  = 'Сработал триггер. Остутствует адрес доставки';
	end if;
end//

delimiter ;
              
insert into delivery (orders_id) values (45);  -- проверка триггера



-- создание таблицы логов

drop table if exists logs;

create table logs(
		create_at datetime,
		name_of_table varchar(20),
		id_table int unsigned not null,
		new_name varchar(30))
	    engine=archive;
	   
-- триггер логов в таблице users	   
drop trigger if exists users_log;

delimiter //

create trigger users_log 
	after insert on users
	for each row
	begin
		insert into logs
		    values (now(),'users', new.id, concat(new.firstname, ' ', new.lastname));
	end//

-- триггер логов в таблице catalogs
drop trigger if exists catalogs_log//
	
create trigger catalogs_log 
	after insert on catalogs
	for each row
	begin
		insert into logs
		    values (now(),'catalogs', new.id, new.name);
	end//
	
-- триггер логов в таблице products	
drop trigger if exists products_log//
	
create trigger products_log 
	after insert on products
	for each row
	begin
		insert into logs
		    values (now(),'products', new.id, new.name);
	end//
	
delimiter ;

insert into users(firstname, lastname) values ('Федор', 'Плотников'); -- проверка триггера логов users_log
insert into catalogs(name) values ('Ламинаторы');-- проверка триггера логов catalogs_log
insert into products(name) values ('HP 1010');-- проверка триггера логов products_log	

-- процедура подсчета суммы каждого заказа
drop procedure if exists cp_count_price_orders;

delimiter //

create procedure cp_count_price_orders()
		begin
			select op.orders_id as `order`, 
			concat(u.firstname, ' ',u.lastname) as customer,
			(p.price*op.amount) as `sum`
			  from orders_products op 
              join products p 
              join users u 
              join orders o 
              on op.products_id = p.id
              and u.id = o.user_id
              and o.id = op.orders_id
              group by op.orders_id
              order by op.orders_id 
              ;
			
		end//

delimiter ;

call cp_count_price_orders(); -- проверка процедуры

-- процедура выбора продукции по бренду и наименьшей цене
drop procedure if exists cb_choice_brend_min_price;

delimiter //

create procedure cb_choice_brend_min_price()
		begin
			select b.name as brend_name,
				   p.name as product,
				   min(p.price) as lowest_price
				
			  from brends b 
              join products p 
              join selection_by_brends sbb
              on p.id = sbb.products_id
              and b.id = sbb.brends_id 
              group by b.name
                          
              ;
			
		end//

delimiter ;

call cb_choice_brend_min_price; -- проверка процедуры


















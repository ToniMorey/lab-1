use sakila;

-- 1. How many copies of the film _Hunchback Impossible_ exist in the inventory system? -- count film_id join film where title = Hunchback impossible
select f.title , count(i.film_id) as Count from inventory i left join film f on i.film_id = f.film_id
where title = 'Hunchback impossible';

-- 2. List all films whose length is longer than the average of all the films. -- avg(film.lenght) 
select avg(length) from film;

select title, length from film 
where length > (select avg(length) from film)
order by length desc;

-- 3. Use subqueries to display all actors who appear in the film _Alone Trip_.
-- select concat(first_name,' ',second_name) from actor where actor_id in film_actor on fa.film_id = f.film_id where title = 'alone trip'
select concat(first_name,' ',last_name) as name from actor
where actor_id in (select actor_id from film_actor
	where actor_id in (select actor_id from film 
			where title = 'alone trip') );
-- no se si está bien pero me ha salido a la primera y no quiero tocar nada. 


-- 4. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
-- select title from film where film_id in film_category where category_id in category where name = family
select title from film 
where film_id in (select film_id from film_category 
	where category_id in (select category_id from category where name = 'family'));

-- 5. Get name and email from customers from Canada using subqueries. Do the same with joins. 
-- Note that to create a join, you will have to identify the correct tables with their primary keys and foreign keys, that will help you get the relevant information.
select first_name, email from customer 
where address_id in (select address_id from address 
	where city_id in (select city_id from city 
		where country_id in (select country_id from country
			where country = 'Canada')));

select first_name, email from 
customer c left join address a on c.address_id = a.address_id
left join city ci on a.city_id = ci.city_id
left join country co on ci.country_id = co.country_id
where country = 'Canada';


-- 6. Which are films starred by the most prolific actor? Most prolific actor is defined as the actor that has acted in the most number of films.
-- First you will have to find the most prolific actor and then use that actor_id to find the different films that he/she starred.


select max(cuenta) from (
select count(actor_id) as cuenta from film_actor
group by actor_id
order by count(actor_id) desc) sub1 ; -- Seleccionamos el máximo de veces que un actor aparece en una peli

select actor_id as id from film_actor
group by actor_id
having count(actor_id) = (select max(cuenta) from (
	select count(actor_id) as cuenta from film_actor
	group by actor_id
	order by count(actor_id) desc) sub1); -- Seleccionamos el id del actor que tiene el máximo de veces apareciendo en una peli


select film_id from film_actor where actor_id in 
(select actor_id as id from film_actor
group by actor_id
having count(actor_id) = (select max(cuenta) from (
	select count(actor_id) as cuenta from film_actor
	group by actor_id
	order by count(actor_id) desc) sub1)); -- Seleccionamos aquellas pelis (ID) donde aparece el actor

select title from film 
where film_id in (select film_id from film_actor where actor_id in 
(select actor_id as id from film_actor
group by actor_id
having count(actor_id) = (select max(cuenta) from (
	select count(actor_id) as cuenta from film_actor
	group by actor_id
	order by count(actor_id) desc) sub1))); -- Seleccionamos los títulos que aparecen en la lista anterior

-- 7. Films rented by most profitable customer. 
-- You can use the customer table and payment table to find the most profitable customer ie the customer that has made the largest sum of payments
select max(monto) from (
select sum(amount) as monto from payment
group by customer_id) sub1; -- maximo amount por customer

select customer_id from payment
group by customer_id 
having sum(amount) = (select max(monto) from (
select sum(amount) as monto from payment
group by customer_id) sub1); -- customer con el máximo amount

select inventory_id from rental 
where customer_id = (select customer_id from payment
group by customer_id 
having sum(amount) = (select max(monto) from (
select sum(amount) as monto from payment
group by customer_id) sub1)); -- inventory_id de las pelis que ha rentado el customer

select film_id from inventory 
where inventory_id in (select inventory_id from rental 
where customer_id = (select customer_id from payment
group by customer_id 
having sum(amount) = (select max(monto) from (
select sum(amount) as monto from payment
group by customer_id) sub1))); -- el film ID correspondiente al inventory ID de esas pelis

select title from film 
where film_id in (select film_id from inventory
	where inventory_id in (select inventory_id from rental 
		where customer_id = (select customer_id from payment
		group by customer_id 
			having sum(amount) = (select max(monto) from (
			select sum(amount) as monto from payment
				group by customer_id) sub1)))); -- No entiendo por qué me salen solo 44 rows y no 45 como antes

-- 8. Get the `client_id` and the `total_amount_spent` of those clients who spent more than the average of the `total_amount` spent by each client.

select (sum(amount)/count(distinct customer_id)) as avg_amount_spend from payment;

select customer_id , sum(amount) from payment 
group by customer_id
having sum(amount) >= (select (sum(amount)/count(distinct customer_id)) as avg_amount_spend from payment);



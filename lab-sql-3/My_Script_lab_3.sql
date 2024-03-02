use sakila;
-- 1. How many distinct (different) actors' last names are there?
select count(distinct last_name) from sakila.actor;

-- 2. In how many different languages where the films originally produced? (Use the column `language_id` from the `film` table)
select count(distinct language_id) from sakila.film;

-- 3. How many movies were released with `"PG-13"` rating?
select count(rating) from sakila.film
where rating = 'PG-13';

-- 4. Get 10 the longest movies from 2006.
select title, length from sakila.film
order by length desc
limit 10;

-- 5. How many days has been the company operating (check `DATEDIFF()` function)?
select datediff(max(rental_date), min(rental_date)) from sakila.rental;

-- 6. Show rental info with additional columns month and weekday. Get 20.
select rental_id, rental_date, 
date_format(rental_date, '%M') as rental_Month, date_format(rental_date, '%d') as rental_day , inventory_id, customer_id, return_date,
date_format(return_date, '%M') as return_Month, date_format(return_date, '%d') as return_day ,staff_id , last_update ,
date_format(last_update, '%M') as update_Month, date_format(last_update, '%d') as update_day 
from sakila.rental
limit 20;

-- 7. Add an additional column `day_type` with values 'weekend' and 'workday' depending on the rental day of the week.
select rental_id, rental_date, 
date_format(rental_date, '%M') as rental_Month, date_format(rental_date, '%d') as rental_day, if(date_format(rental_date,'%a') = 'sun' or 'sat', 'weekend', 'workday') as rental_day_type, inventory_id, customer_id, return_date,
date_format(return_date, '%M') as return_Month, date_format(return_date, '%d') as return_day ,if(date_format(return_date,'%a') = 'sun' or 'sat', 'weekend', 'workday') as return_day_type ,staff_id , last_update ,
date_format(last_update, '%M') as update_Month, date_format(last_update, '%d') as update_day ,if(date_format(last_update,'%a') = 'sun' or 'sat', 'weekend', 'workday') as last_update_day_type
from sakila.rental;

-- 8. How many rentals were in the last month of activity?
select rental_date from sakila.rental
order by rental_date desc;

select count(rental_date) from sakila.rental
where date_format(rental_date, '%M') = 'february' and date_format(rental_date, '%Y') = 2006;


-- Mi idea, pero no lo he sabido hacer: ¿Como se puede hacer? No me gusta que en la parte de arriba se tenga que especificar el mes y el año.
select sum(
			if(
				concat(
					date_format(rental_date,'%Y') , date_format(rental_date,'%M')) 
                    =
                    max(
						concat(
							date_format(rental_date,'%Y') , date_format(rental_date,'%M'))),1,0)) from sakila.rental;

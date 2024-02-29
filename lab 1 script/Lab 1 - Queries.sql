-- 1. Use sakila database. OK

-- 2. Get all the data from tables `actor`, `film` and `customer`.
select * from sakila.actor;
select * from sakila.film;
select * from sakila.customer;

-- 3. Get film titles.
select distinct title from sakila.film;

-- 4. Get unique list of film languages under the alias `language`. Note that we are not asking you to obtain the language per each film, but this is a good time to think about how you might get that information in the future.
select distinct name from sakila.language;
-- 5.
-- - 5.1 Find out how many stores does the company have?
select count(store_id) from sakila.store;
--  - 5.2 Find out how many employees staff does the company have?
 select count(staff_id) from sakila.staff;
--  - 5.3 Return a list of employee first names only?
select first_name from sakila.staff;
-- 6. Select all the actors with the first name ‘Scarlett’.
select actor_id, first_name, last_name from sakila.actor where first_name = 'Scarlett';
-- 7. Select all the actors with the last name ‘Johansson’.
select actor_id, first_name, last_name from sakila.actor where last_name = 'Johansson';
-- 8. How many films (movies) are available for rent?
select count(film_id) from sakila.film;
-- 9. What are the shortest and longest movie duration? Name the values max_duration and min_duration.
select max(length) as max_duration, min(length) as min_duration from sakila.film;
-- 10. What's the average movie duration?
select avg(length) as average_duration from sakila.film;
-- 11. How many movies are longer than 3 hours?
select count(film_id) as 'longer than 3 hour' from sakila.film where (length/60 > 3);
-- 12. What's the length of the longest film title?
select max(length(title)) as 'longest film title' from sakila.film;
use sakila;
-- 1. Rank films by length (filter out the rows with nulls or zeros in length column). Select only columns title, length and rank in your output.
select title, length, rank() over(order by length desc) from sakila.film
where length is not null and length > 0;

-- 2. Rank films by length within the `rating` category (filter out the rows with nulls or zeros in length column). In your output, only select the columns title, length, rating and rank. 
select title, rating, length, rank() over(order by length desc) from sakila.film
where length is not null and length > 0;
 
-- 3. How many films are there for each of the categories in the category table? **Hint**: Use appropriate join between the tables "category" and "film_category".
select c.name , count(f.category_id) from film_category f left join category c on f.category_id = c.category_id
group by c.name;

-- 4. Which actor has appeared in the most films? **Hint**: You can create a join between the tables "actor" and "film actor" and count the number of times an actor appears.
select count(f.actor_id), concat(a.first_name, ' ', a.last_name) from film_actor f left join actor a on f.actor_id = a.actor_id
group by concat(a.first_name, ' ', a.last_name)
order by count(f.actor_id) desc
limit 1;

-- 5. Which is the most active customer (the customer that has rented the most number of films)? 
-- **Hint**: Use appropriate join between the tables "customer" and "rental" and count the `rental_id` for each customer.
select concat(c.first_name,' ', c.last_name), count(r.rental_id) from rental r left join customer c on r.customer_id = c.customer_id
group by concat(c.first_name,' ', c.last_name)
order by count(r.rental_id) desc
limit 1;

-- 6. List the number of films per category.
select c.name , count(f.category_id) from film_category f left join category c on f.category_id = c.category_id
group by c.name;

-- 7. Display the first and the last names, as well as the address, of each staff member.
select concat(s.first_name, ' ',s.last_name), a.address from staff s left join address a on s.address_id=a.address_id
group by concat(s.first_name, ' ',s.last_name), a.address;

-- 8. Display the total amount rung up by each staff member in August 2005.
select concat(s.first_name, ' ',s.last_name), sum(p.amount) from payment p left join staff s on p.staff_id = s.staff_id
where date_format(payment_date,'%M') = 'August' and date_format(payment_date,'%Y') = 2005
group by concat(s.first_name, ' ',s.last_name);

-- 9. List all films and the number of actors who are listed for each film.
select f.title, count(fa.actor_id) from film_actor fa left join film f on fa.film_id = f.film_id
group by f.title
order by count(fa.actor_id) desc;

-- 10. Using the payment and the customer tables as well as the JOIN command, list the total amount paid by each customer. 
-- List the customers alphabetically by their last names.
select concat(c.first_name,' ',c.last_name), sum(p.amount) from customer c left join payment p on c.customer_id = p.customer_id
group by concat(c.first_name,' ',c.last_name), last_name
order by c.last_name;

-- 11. Write a query to display for each store its store ID, city, and country. -- adress_id from store join to address for city_id join to city for country id join to country
select s.store_id, c.city, co.country 
from store s left join address a on s.address_id = a.address_id
left join city c on a.city_id = c.city_id
left join country co on c.country_id = co.country_id;

-- 12. Write a query to display how much business, in dollars, each store brought in.
select s.store_id , sum(p.amount) from payment p 
left join staff f on p.staff_id=f.staff_id 
left join store s on s.store_id=f.store_id
group by s.store_id;

-- 13. What is the average running time of films by category?
select c.name , avg(f.length) from film f left join film_category fc on f.film_id = fc.film_id
left join category c on fc.category_id = c.category_id
group by c.name;

-- 14. Which film categories are longest?
select c.name , avg(f.length) from film f left join film_category fc on f.film_id = fc.film_id
left join category c on fc.category_id = c.category_id
group by c.name
order by avg(f.length) desc
limit 5;

-- 15. Display the most frequently rented movies in descending order. title in film- inventory_id  -rental_id in rental
select f.title, count(r.rental_id) from rental r left join inventory i on r.inventory_id = i.inventory_id left join film f on i.film_id = f.film_id
group by f.title
order by count(r.rental_id) desc;

-- 16. List the top five genres in gross revenue in descending order. - amount(payment) - staff_id - store_id - film_category- category_id on name(category)
select c.name ,sum(p.amount) 
from payment p left join rental r on p.staff_id = r.staff_id
left join inventory i on r.inventory_id = i.inventory_id
left join film_category f on i.film_id=f.film_id
left join category c on c.category_id = f.category_id
group by c.name
order by sum(p.amount)
limit 5;

-- 17. Is "Academy Dinosaur" available for rent from Store 1?
select f.title , sto.store_id from film f left join inventory i on f.film_id=i.film_id
left join rental r on i.inventory_id = r.inventory_id
left join staff st on r.staff_id = st.staff_id 
left join store sto on st.staff_id = sto.store_id
where title = 'academy dinosaur' and sto.store_id = 1
group by sto.store_id, f.title;



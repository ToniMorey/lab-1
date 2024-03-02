use sakila;
-- 1. Get film ratings.
select title, rating from sakila.film;
select distinct rating from sakila.film;

-- 2. Get release years.
select title, release_year from sakila.film;
select distinct release_year from sakila.film;

-- 3. Get all films with ARMAGEDDON in the title.
select title from sakila.film
where title regexp 'armageddon';

-- 4. Get all films with APOLLO in the title
select title from sakila.film
where title regexp 'apollo';

-- 5. Get all films which title ends with APOLLO.
select title from sakila.film
where title regexp 'apollo$';

-- 6. Get all films with word DATE in the title.
select title from sakila.film
where title regexp '^date | date$| date '; -- Así cubro todas las posibildades de que tenga SOLO la palabra date y no palabras formadas con date (como candidate)


-- 7. Get 10 films with the longest title.
select title from sakila.film
order by length(title) desc
limit 10;

-- 8. Get the 10 longest films.
select title from sakila.film
order by length desc
limit 10;

-- 9. How many films include **Behind the Scenes** content?
select count(title) from sakila.film
where special_features regexp 'Behind the scenes';

-- 10. List films ordered by release year and title in alphabetical order.
select title , release_year from sakila.film
order by title asc;

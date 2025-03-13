-- Задание 2

-- Название и продолжительность самого длительного трека.
select name, duration 
from tracks t 
where duration = (select max(duration) from tracks);

-- Название треков, продолжительность которых не менее 3,5 минут.
select name
from tracks
where duration >= 210

-- Названия сборников, вышедших в период с 2018 по 2020 год включительно.
select title 
from compilations 
where year >= 2018 and year <=2020

-- Исполнители, чьё имя состоит из одного слова.
select name 
from artists 
where name NOT LIKE '% %';

-- Название треков, которые содержат слово «мой» или «my».
select name
from tracks
where name ~* '\mmy\M' OR name ~* '\mмой\M';;


-- Задание 3
-- Количество исполнителей в каждом жанре.
select g.name, count (ga.artist_id) as artist_count
from genres g 
left join genre_artists ga on g.id = ga.genre_id 
group by g.name 

-- Количество треков, вошедших в альбомы 2019–2020 годов.
select count(t.id) as track_count
from tracks t 
join albums a on t.album_id = a.id  
where a.release_year  between 2019 and 2020

-- Средняя продолжительность треков по каждому альбому.
select a.name as album_title, avg(t.duration) as avg_duration 
from tracks t
join albums a on t.album_id = a.id 
group by a.name 

-- Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT a.name AS artist_name
FROM artists a
WHERE a.id NOT IN (
    SELECT aa.artist_id
    FROM artist_albums aa
    JOIN albums al ON aa.album_id = al.id
    WHERE al.release_year = 2020
);

-- Названия сборников, в которых присутствует конкретный исполнитель (Пётр Лещенко).
SELECT DISTINCT c.title AS collection_title
FROM compilations c 
JOIN compilationtracks c2 ON c.id = c2.compilation_id
JOIN tracks t ON c2.track_id = t.id
JOIN albums al ON t.album_id = al.id
JOIN artist_albums aa ON al.id = aa.album_id
JOIN artists a ON aa.artist_id = a.id
WHERE a.name = 'Пётр Лещенко';






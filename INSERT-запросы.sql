-- INSERT-запросы (задание 1)
insert into genres (name)
values('Поп-жанр'),
	('R&B'),
      ('Кантри'),
      ('Русский шансон');

insert into artists (name)
values('Пётр Лещенко'), 
	('Билл Монро'), 
	('Alicia'), 
      ('Мартин Гаррикс'); 

insert into albums (name, release_year)
values('Всё, что было', 1988),
	('Блюз Собачьего Дома', 2001),
	('Animals', 2019),
      ('New Day', 1997);

insert  into tracks (name, duration, album_id )
values('Осенний мираж', 250, 1),
	('Я Увидел Свет', 100, 2),
	('Блюз Скалистой Дороги', 150, 2),
	('Russian Roulette', 200, 4),
	('Haegeum my', 350, 3),
      ('my own', 340, 4),
      ('own my', 350, 3),
      ('my', 300, 1),
      ('myself', 320, 2),
      ('by myself', 250, 3),
      ('Running Wild', 100, 4);

insert into genre_artists (genre_id, artist_id)
values(1, 1),
      (2, 2),
      (3, 3),
      (4, 4);

insert  into artist_albums (artist_id, album_id)
values(1, 1),
      (2, 2),
      (3, 3),
      (4, 4);

insert into compilations (title, year)
values('сборник-1', 2018),
      ('сборник-2', 2022),
      ('сборник-3', 2020),
      ('сборник-4', 2024);

insert  into compilationtracks (compilation_id, track_id)
values(1, 1),
      (2, 1),
      (3, 3),
      (4, 6);





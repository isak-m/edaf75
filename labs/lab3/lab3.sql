PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theatres;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS screenings;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS customers;

PRAGMA foreign_keys=ON;

CREATE TABLE theatres (
   	th_name		TEXT,
	capacity	INT,
	PRIMARY KEY (th_name)
);


CREATE TABLE movies (
    m_title		TEXT,
    production_year	INT,
    imdb_key		TEXT,
    running_time	INT,
    PRIMARY KEY (imdb_key)
);


CREATE TABLE screenings(
    sc_id	TEXT DEFAULT (lower(hex(randomblob(16)))),
    sc_date     DATE,
    start_time	TIME,
    th_name     TEXT,
    imdb_key	TEXT,
--    remainingSeats	INT,
    FOREIGN KEY (th_name) REFERENCES theatres(th_name),
    FOREIGN KEY (imdb_key) REFERENCES movies(imdb_key),
    PRIMARY KEY (sc_id)
);

CREATE TABLE tickets(
    ti_id	TEXT  DEFAULT (lower(hex(randomblob(16)))),
    username    TEXT,
    sc_id	TEXT NOT NULL,
    FOREIGN KEY (sc_id)	   REFERENCES screenings(sc_id),
    FOREIGN KEY (username) REFERENCES customers(username),
    PRIMARY KEY (ti_id)
);


CREATE TABLE customers(
    username    TEXT,
    full_name   TEXT,
    c_password	TEXT,
    PRIMARY KEY (username)
);


INSERT OR IGNORE
INTO movies(m_title, production_year, imdb_key, running_time)
VALUES  ('Marriage Story', 2019, 'tt7653254', 140),
        ('Jojo Rabbit', 2019, 'tt2584384', 100),
        ('Total Recall', 1990, 'tt0100802', 113),
        ('Polis ger servitris 2 miljoner i dricks', 1994, 'tt0110167', 101),
        ('Citizen Kane', 1941, 'tt0033467', 119),
        ('Arrival', 2016, 'tt2543164', 116),
        ('1917', 2019, 'tt8579674', 119),
        ('Once Upon a Time... in Hollywood', 2019, 'tt7131622', 161),
        ('Forrest Gump', 1994, 'tt0109830', 142),
        ('The Irishman', 2019, 'tt1302006', 209),
        ('Uncut Gems', 2019, 'tt5727208', 135),
        ('Stalker', 1979, 'tt0079944', 162),
        ('Metropolis', 1927, 'tt0017136', 153),
        ('Scener ur ett äktenskap', 1974, 'tt6725014', 169),
        ('The Deer Hunter', 1978, 'tt0077416', 183),
        ('The Room', 2003, 'tt0368226', 99),
        ('Porträtt av en kvinna i brand', 2019, 'tt8613070', 121),
        ('The Lighthouse', 2019, 'tt7984734', 109),
        ('The Farewell', 2019, 'tt8637428', 100),
        ('The Neighbors Window', 2019, 'tt8163822', 21),
        ('A Sister', 2018, 'tt8767544', 17);

INSERT OR IGNORE
INTO theatres(th_name, capacity)
VALUES ('Rigoletto', 250),
       ('Skandia', 170),
       ('Sergel', 360),
       ('Saga', 220),
       ('Victoria', 110);
       
INSERT OR IGNORE
INTO customers(username, full_name, c_password)
VALUES  ('Krusbaer', 'Kerstin Brökås', '123123123'),
        ('Bibby_13', 'Mats Snickelback', 'p4ssw0rd'),
        ('Namnam', 'Harald Fossing', '777777777'),
        ('Dragon_slayer', 'Maj Stråle', 'woodstock69'),
        ('Woopie55', 'Chris Gregerflöjt', '0o0o0o0o');
        
INSERT OR IGNORE
INTO screenings(sc_date, start_time, th_name, imdb_key)
VALUES ('2020-02-14', '10:00', 'Skandia', 'tt7653254'),
       ('2020-02-14', '13:00', 'Skandia', 'tt2584384'),
       ('2020-02-14', '17:00', 'Skandia', 'tt0100802'),
       ('2020-02-14', '20:00', 'Skandia', 'tt0110167'),
       ('2020-02-14', '23:00', 'Skandia', 'tt0033467'),
       ('2020-02-15', '10:00', 'Skandia', 'tt2543164'),
       ('2020-02-15', '13:00', 'Skandia', 'tt8579674'),
       ('2020-02-15', '17:00', 'Skandia', 'tt7131622'),
       ('2020-02-15', '20:00', 'Skandia', 'tt0109830'),
       ('2020-02-15', '23:00', 'Skandia', 'tt1302006'),
       ('2020-02-16', '10:00', 'Skandia', 'tt6725014'),
       ('2020-02-16', '13:00', 'Skandia', 'tt7984734'),
       ('2020-02-16', '17:00', 'Skandia', 'tt5727208'),
       ('2020-02-16', '20:00', 'Skandia', 'tt0079944'),
       ('2020-02-16', '23:00', 'Skandia', 'tt7653254'),
       ('2020-02-14', '10:00', 'Rigoletto', 'tt2584384'),
       ('2020-02-14', '13:00', 'Rigoletto', 'tt2543164'),
       ('2020-02-14', '17:00', 'Rigoletto', 'tt1302006'),
       ('2020-02-14', '20:00', 'Rigoletto', 'tt0017136'),
       ('2020-02-14', '23:00', 'Rigoletto', 'tt0077416'),
       ('2020-02-15', '10:00', 'Rigoletto', 'tt2584384'),
       ('2020-02-15', '13:00', 'Rigoletto', 'tt2543164'),
       ('2020-02-15', '17:00', 'Rigoletto', 'tt1302006'),
       ('2020-02-15', '20:00', 'Rigoletto', 'tt0017136'),
       ('2020-02-15', '23:00', 'Rigoletto', 'tt0077416'),
       ('2020-02-16', '10:00', 'Rigoletto', 'tt2584384'),
       ('2020-02-16', '13:00', 'Rigoletto', 'tt2543164'),
       ('2020-02-16', '17:00', 'Rigoletto', 'tt1302006'),
       ('2020-02-16', '20:00', 'Rigoletto', 'tt0017136'),
       ('2020-02-16', '23:00', 'Rigoletto', 'tt0077416'),
       ('2020-02-14', '10:00', 'Sergel', 'tt8767544'),
       ('2020-02-14', '13:00', 'Sergel', 'tt8163822'),
       ('2020-02-14', '17:00', 'Sergel', 'tt0368226'),
       ('2020-02-14', '20:00', 'Sergel', 'tt0079944'),
       ('2020-02-14', '23:00', 'Sergel', 'tt2543164'),
       ('2020-02-15', '10:00', 'Sergel', 'tt8767544'),
       ('2020-02-15', '13:00', 'Sergel', 'tt8163822'),
       ('2020-02-15', '17:00', 'Sergel', 'tt0368226'),
       ('2020-02-15', '20:00', 'Sergel', 'tt0017136'),
       ('2020-02-15', '23:00', 'Sergel', 'tt0077416'),
       ('2020-02-16', '10:00', 'Sergel', 'tt2584384'),
       ('2020-02-16', '13:00', 'Sergel', 'tt8767544'),
       ('2020-02-16', '17:00', 'Sergel', 'tt1302006'),
       ('2020-02-16', '20:00', 'Sergel', 'tt0017136'),
       ('2020-02-16', '23:00', 'Sergel', 'tt0079944'),
       ('2020-02-14', '10:00', 'Saga', 'tt7653254'),
       ('2020-02-14', '13:00', 'Saga', 'tt8767544'),
       ('2020-02-14', '17:00', 'Saga', 'tt8163822'),
       ('2020-02-14', '20:00', 'Saga', 'tt8637428'),
       ('2020-02-14', '23:00', 'Saga', 'tt7984734'),
       ('2020-02-15', '10:00', 'Saga', 'tt8613070'),
       ('2020-02-15', '13:00', 'Saga', 'tt0368226'),
       ('2020-02-15', '17:00', 'Saga', 'tt0077416'),
       ('2020-02-15', '20:00', 'Saga', 'tt0077416'),
       ('2020-02-15', '23:00', 'Saga', 'tt6725014'),
       ('2020-02-16', '10:00', 'Saga', 'tt0079944'),
       ('2020-02-16', '13:00', 'Saga', 'tt1302006'),
       ('2020-02-16', '17:00', 'Saga', 'tt7131622'),
       ('2020-02-16', '20:00', 'Saga', 'tt2543164'),
       ('2020-02-16', '23:00', 'Saga', 'tt0033467'),
       ('2020-02-14', '10:00', 'Victoria', 'tt7653254'),
       ('2020-02-14', '13:00', 'Victoria', 'tt8767544'),
       ('2020-02-14', '17:00', 'Victoria', 'tt8163822'),
       ('2020-02-14', '20:00', 'Victoria', 'tt0077416'),
       ('2020-02-14', '23:00', 'Victoria', 'tt7984734'),
       ('2020-02-15', '10:00', 'Victoria', 'tt8613070'),
       ('2020-02-15', '13:00', 'Victoria', 'tt7653254'),
       ('2020-02-15', '17:00', 'Victoria', 'tt0033467'),
       ('2020-02-15', '20:00', 'Victoria', 'tt0077416'),
       ('2020-02-15', '23:00', 'Victoria', 'tt6725014'),
       ('2020-02-16', '10:00', 'Victoria', 'tt0079944'),
       ('2020-02-16', '13:00', 'Victoria', 'tt7653254'),
       ('2020-02-16', '17:00', 'Victoria', 'tt7131622'),
       ('2020-02-16', '20:00', 'Victoria', 'tt7653254'),
       ('2020-02-16', '23:00', 'Victoria', 'tt0077416');



DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id integer primary key autoincrement,
  name string not null,
  email string not null
);


CREATE TABLE sorting_results (
  id integer primary key autoincrement,
  number_of_elements integer not null,
  sorting_algorithm string not null,
  time_of_execution float not null,
);



CREATE TABLE "sorting_results" (
	"id"	INTEGER NOT NULL,
	"number_of_elements"	INTEGER NOT NULL,
	"sorting_algorithm"	TEXT NOT NULL,
	"time_of_execution"	NUMERIC NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
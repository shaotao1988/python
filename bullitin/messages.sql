create table messages(
	id		 INT NOT null AUTO_INCREMENT,
	subject  varchar(100) not null,
	sender   varchar(15) not null,
	reply_to int,
	text     mediumtext not null,
	primary key (id)
);
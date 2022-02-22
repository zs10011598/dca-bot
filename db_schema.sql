-- dca_bot_db

CREATE TABLE price(id serial, 
	high double precision, 
	last double precision, 
	created_at timestamp,
	book varchar(10),
	volume double precision,
	vwap double precision,
	low double precision,
	ask double precision,
	bid double precision,
	change_24 double precision,
	exchange varchar(10),
	datetime_request timestamp default current_timestamp);

CREATE INDEX idx_price_datetime_request ON price(datetime_request); 
CREATE INDEX idx_price_created_at ON price(created_at);
CREATE INDEX idx_price_exchange ON price(exchange);


CREATE TABLE transaction(id serial,
	bot_id varchar(30),
	cycle integer default 1,
	datetime_request timestamp default current_timestamp);


CREATE TABLE parameter(id serial,
	key varchar(50),
	value varchar(50),
	datatype varchar(10));

CREATE INDEX idx_parameter_key ON parameter(key); 

INSERT INTO parameter(key, value, datatype) VALUES('keep', 'True', 'boolean');
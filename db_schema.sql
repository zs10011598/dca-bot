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
	transaction_index integer default 1,
	transaction_datetime timestamp default current_timestamp,
	type_operation varchar(4) default 'buy',
	entry_price double precision,
	transaction_fee double precision,
	transaction_currency_ammount double precision,
	cummulated_currency_ammount double precision,
	average_price double precision,
	profit double precision);

CREATE INDEX idx_transaction_bot_id ON transaction(bot_id);
CREATE INDEX idx_transaction_transaction_datetime ON transaction(transaction_datetime);
CREATE INDEX idx_transaction_type_operation ON transaction(type_operation);
CREATE INDEX idx_transaction_cycle ON transaction(cycle);


CREATE TABLE parameter(id serial,
	key varchar(50),
	value varchar(50),
	datatype varchar(10));

CREATE INDEX idx_parameter_key ON parameter(key); 

INSERT INTO parameter(key, value, datatype) VALUES('keep', 'True', 'boolean');

ALTER TABLE transaction ADD COLUMN cummulated_cryptocurrency_ammount double precision;
ALTER TABLE transaction ADD COLUMN environment varchar(10);
ALTER TABLE transaction ADD COLUMN order_id varchar(20);
ALTER TABLE transaction ADD COLUMN exchange varchar(10);
ALTER TABLE transaction ADD COLUMN transaction_cryptocurrency_fee double precision;
ALTER TABLE transaction RENAME COLUMN transaction_fee TO transaction_currency_fee;
ALTER TABLE transaction ADD COLUMN transaction_cryptocurrency_ammount double precision;
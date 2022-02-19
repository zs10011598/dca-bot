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
	datetime_request timestamp default current_timestamp);

CREATE INDEX idx_price_datetime_request ON price(datetime_request); 
CREATE INDEX idx_price_created_at ON price(created_at);
INSERT INTO price(
	high, 
	last, 
	created_at, 
	book,
	volume,
	vwap,
	low,
	ask,
	bid,
	change_24,
	exchange)
VALUES (
	{high},
	{last},
	'{created_at}',
	'{book}',
	{volume},
	{vwap},
	{low},
	{ask},
	{bid},
	{change_24},
	'{exchange}'
)
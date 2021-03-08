create table raw.monthly_prices (
	market_date date,
	open_price numeric(20,6), 
	high_price numeric(20,6), 
	low_price numeric(20,6), 
	close_price numeric(20,6), 
	volume numeric(20,6), 
	dividends numeric(20,6), 
	stock_splits numeric(20,6), 
	ticker varchar(10)
)
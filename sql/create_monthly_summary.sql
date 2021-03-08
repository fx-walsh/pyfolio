create table raw.monthly_summary (
	ticker varchar(10),
    year_month varchar(7),
    lowest_close numeric(20,6), 
    highest_close numeric(20,6), 
    avg_close numeric(20,6), 
    lowest_open numeric(20,6), 
    highest_open numeric(20,6),
    avg_open numeric(20,6),                              
    highest_high numeric(20,6), 
    lowest_low numeric(20,6), 
    daily_return_volatility numeric(20,6), 
    avg_daily_return numeric(20,6), 
    monthly_return numeric(20,6),
    total_price_change numeric(20,6), 
    daily_volume_volatility numeric(20,6), 
    avg_volume_change numeric(20,6), 
    monthly_perc_volume_change numeric(20,6),
    total_volume_change numeric(20,6)
)
;

use TFB103d_project;

create table company_factor(
data_date varchar(36),
stock_code varchar(36),
change_rate_bys float(4,2) default 0,
avg_board_bys float(4,2) default 0,
avg_director_rate float(4,2) default 0,
foreign_rate_bys float(4,2) default 0,
over1000_rate_bys float(4,2) default 0,
under400_rate_bys float(4,2) default 0
);
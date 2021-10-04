use covid;
create table covidseason(
	iso_code varchar(24) comment '國碼',
    location varchar(24) comment '國家',
    date_season varchar(24) comment '年季',
    new_cases int default 0 comment '新增確診數',
    new_cases_smoothed float(10,2) default 0.0 comment '七天移動平均新增確診數'
);
drop table covidseason;
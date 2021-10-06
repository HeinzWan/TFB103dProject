use covid;
create table covidseason(
	iso_code varchar(24) comment '國碼',
    location varchar(24) comment '國家',
    date_season varchar(24) comment '年季',
    new_cases_smoothed float(10,2) default 0.0 comment '七天移動平均新增確診數',
    reproduction_rate float(10,2) default 0.0 comment '傳染率',
    positive_rate float(10,2) default 0.0 comment '陽性率',
    people_fully_vaccinated_per_hundred float(10,2) default 0.0 comment '每百人接種疫苗人數'
);
drop table covidseason;
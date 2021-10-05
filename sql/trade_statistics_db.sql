create database tradedb;
use tradedb;
create table tradestatistics(
	imports_exports varchar(24) comment '進出口別',
    date_t varchar(24) comment '日期',
    commodity_code varchar(24) comment '貨品號列',
    chinese_description_good varchar(200) comment '中文貨名',
    engish_description_good varchar(200) comment '英文貨名',
    usd_value integer comment '美元(千元)',
    ntd_value integer comment '新台幣(千元)',
    tne_weight integer comment '重量(公噸)',
    kgm_weight integer comment '重量(公斤)'
);
drop table tradestatistics;

create table tradeseason(
	imports_exports varchar(24) comment '進出口別',
    date_season varchar(24) comment '年季',
    commodity_code varchar(24) comment '貨品號列',
    chinese_description_good varchar(200) comment '中文貨名',
    engish_description_good varchar(200) comment '英文貨名',
    usd_value integer comment '美元(千元)',
    ntd_value integer comment '新台幣(千元)',
    tne_weight integer comment '重量(公噸)',
    kgm_weight integer comment '重量(公斤)'
);
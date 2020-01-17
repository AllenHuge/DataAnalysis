CREATE TABLE IF NOT EXISTS `stock_quotation_his`(
	id BIGINT UNSIGNED AUTO_INCREMENT
    ,trade_date		DATE
	,pre_close		DOUBLE
	,open			DOUBLE
	,high	    	DOUBLE
	,low	        DOUBLE
	,close	    	DOUBLE
	,volume			DOUBLE
	,amt			DOUBLE
	,dealnum		BIGINT
	,chg			DOUBLE
	,pct_chg		DOUBLE
	,swing			DOUBLE
	,PRIMARY KEY ( id )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
create table tKeyVal  (
	skey  varchar(32) not null,
    skey0  varchar(32) not null,
    cval  varchar(1024) not null,
	cdate  timestamp without time zone,
	
  
);
ALTER TABLE tKeyVal ADD CONSTRAINT tkeyval_pkey PRIMARY KEY(skey0,cdate);
CREATE UNIQUE INDEX skey0_cdate ON tKeyVal (skey,cdate);
#ALTER TABLE tKeyVal ADD COLUMN skey0 varchar(32);
DROP INDEX skey_cdate



REVOKE ALL ON TABLE tKeyVal FROM  select_insert_only;
GRANT SELECT,Insert ON TABLE tKeyVal TO  select_insert_only;

#update tKeyVal set skey0=skey where cdate >= '2019-05-30 00:00:00';

###################################################################
create table tTest  (
	command varchar(256) not null
	#sdate  timestamp without time zone not null,
	#edate   timestamp without time zone
  
);
-- alter table [sel_containers] add name varchar(100);
-- alter table [sel_containers] add company varchar(100);
-- alter table [sel_containers] add phone varchar(20); 
-- alter table [sel_containers] add flag varchar(1);


drop view movimat;
 CREATE VIEW movimat AS
 select ROW_NUMBER() OVER (ORDER BY ((select max(pickTime) from sel_pick_details p where pickContainerId = containerId) - (select min(pickTime) from sel_pick_details p where pickContainerId = containerId))) as row, 
		containerNumber, 
		name , 
		company, 
		phone,
		substring(CONVERT(VARCHAR(10),((select max(pickTime) from sel_pick_details p where pickContainerId = containerId) - (select min(pickTime) from sel_pick_details p where pickContainerId = containerId)),108),4,5) as ptime
	from sel_containers c 
	where status = 3
		AND name is not null
		AND flag is null



-- select TOP 1 * from [VLDemo].[dbo].[sel_containers] where name is NULL OR name = '';


-- select * from [VLDemo].[dbo].[sel_containers]



-- select name, company, phone from sel_containers where flag is null and status = 3
-- update sel_containers set flag = 1


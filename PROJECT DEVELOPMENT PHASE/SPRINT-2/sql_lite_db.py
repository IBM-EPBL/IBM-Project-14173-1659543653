import sqlite3  

def sql_lite_db():
    # Create DB if not exists and Connect to the DB
    conn = sqlite3.connect('plasmadatabase.db')

    # Table DDL Scripts
    create_tables =  ['create table  if not exists pd_user_data ( pdapp_username TEXT ,email TEXT ,phone TEXT ,user_addess TEXT ,dob date, covid19_status TEXT );',
    'create table  if not exists pd_donors (pdapp_username TEXT ,blood_group_With_RH TEXT ,donation_signedup_date date ,last_donated_date date );',
    'create table  if not exists pd_requests ( pdapp_username TEXT ,blood_group_With_RH TEXT,requested_for_address TEXT ,requested_date date ,request_status TEXT);',
    'create table  if not exists pd_app_user_creds ( pdapp_username TEXT ,pdapp_password TEXT );']

    # Inset Data
    insert_data = [
    "Insert into pd_requests values ('srinu57','A RhD positive (A+)','H.No: 34 Mambalam Chennai 600023','2022-10-6','Open');","Insert into pd_requests values ('srinu57','AB RhD negative (AB-)','H.No: 100 Poondamalli Chennai 600025','2022-10-4','Open');","Insert into pd_requests values ('suresh120','B RhD negative (B-)','H.No: 198 Koembedu Chennai 600037','2022-10-4','Open');","Insert into pd_requests values ('suresh120','A RhD negative (A-)','H.No: 120 T Narag Chennai 600039','2022-10-6','Open');","Insert into pd_requests values ('sitar975','O RhD negative (O-)','H.No: 228 T Narag Chennai 600016','2022-10-7','Open');","Insert into pd_requests values ('balaji23','O RhD negative (O-)','H.No: 114 Poondamalli Chennai 600018','2022-10-7','Open');","Insert into pd_requests values ('mahesh01','O RhD negative (O-)','H.No: 56 Koembedu Chennai 600057','2022-10-1','Closed');","Insert into pd_requests values ('balaji23','A RhD negative (A-)','H.No: 138 T Narag Chennai 600004','2022-10-6','Open');","Insert into pd_requests values ('mahesh01','A RhD positive (A+)','H.No: 234 T Narag Chennai 600033','2022-10-8','Open');","Insert into pd_requests values ('sitar975','B RhD negative (B-)','H.No: 117 T Narag Chennai 600067','2022-10-7','Closed');","Insert into pd_requests values ('sitar975','AB RhD negative (AB-)','H.No: 71 Mambalam Chennai 600064','2022-10-8','Open');","","Insert into pd_donors values('mahesh01','AB RhD negative (AB-)','2022-10-27','2020-9-13');","Insert into pd_donors values('suresh120','AB RhD negative (AB-)','2022-10-11','2022-10-26');","Insert into pd_donors values('balaji23','O RhD positive (O+)','2022-10-9','2022-9-15');","Insert into pd_donors values('srinu57','AB RhD positive (AB+)','2022-10-11','2020-10-12');","Insert into pd_donors values('balu76','A RhD positive (A+)','2022-11-1','2019-1-5');","","insert into pd_app_user_creds values ('mahesh01','VQ300A');","insert into pd_app_user_creds values ('suresh120','NI446K');","insert into pd_app_user_creds values ('balaji23','RF477R');","insert into pd_app_user_creds values ('srinu57','WD546Z');","insert into pd_app_user_creds values ('balu76','JB481O');","insert into pd_app_user_creds values ('sitar975','PL840Q');","insert into pd_app_user_creds values ('hafeez12','ZU563A');","","Insert into pd_user_data Values ('mahesh01','mahesh01@Yahoo.com','974-744-4068','H.No: 78 Mambalam Chennai 600077','1997-12-22');","Insert into pd_user_data Values ('suresh120','suresh120@gmail.com','886-540-7410','H.No: 53 Koembedu Chennai 600095','1980-5-22');","Insert into pd_user_data Values ('balaji23','balaji23@gmail.com','763-664-7317','H.No: 123 Mambalam Chennai 600017','1992-1-10');","Insert into pd_user_data Values ('srinu57','srinu57@live.com','771-396-8496','H.No: 230 T Narag Chennai 600087','1988-11-22');","Insert into pd_user_data Values ('balu76','balu76@live.com','976-159-2142','H.No: 24 T Narag Chennai 600021','1984-10-23');","Insert into pd_user_data Values ('sitar975','sitar975@live.com','710-181-9979','H.No: 178 Koembedu Chennai 600004','1997-8-16');","Insert into pd_user_data Values ('hafeez12','hafeez12@hotmail.com','844-148-2828','H.No: 66 Koembedu Chennai 600037','1988-11-10');"]

    # Create tables
    for ddl in create_tables:
        conn.execute(ddl)

    # Insert Data into table for tetsing
    # for dml in insert_data:
        # conn.execute(dml)

    # Close Connection
    conn.close()
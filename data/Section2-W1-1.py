# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 10:06:56 2022

@author: ssssw
"""
#   import jason/Falsk/mysql.connector
import json
from flask import Flask
import mysql.connector

app=Flask(__name__)    
app.secret_key="sec2week1"
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="website"
    )

with open("taipei-attractions.json","r", encoding="utf-8-sig") as response:
    raw=json.load(response)
lens=len(raw["result"]["results"])
for i in range(lens):  # 
    id=i
    nextPage=i//12
    name=raw["result"]["results"][i]["stitle"]
    category=raw["result"]["results"][i]["CAT2"]
    description=raw["result"]["results"][i]["stitle"][0:32]
    address=raw["result"]["results"][i]["address"]
    transport=raw["result"]["results"][i]["info"]
    mrt=raw["result"]["results"][i]["MRT"]
    latitude=raw["result"]["results"][i]["latitude"]
    longitude=raw["result"]["results"][i]["longitude"]
    picture=raw["result"]["results"][i]["file"]
    images=picture.split("http") # 用split http分開
    for j in range(1,len(images)):
        if images[j].lower().endswith(".jpg") or images[j].lower().endswith(".png"): # 篩選.jpg/.png
            images[j]="http"+images[j] # 還原1st網址到picweb2
        else: images[j]=""; continue
    while '' in images:
        images.remove('')
    images=str(images)
    sql="INSERT INTO taipei_attrations_website(nextPage,name,category,description,address,transport,mrt,latitude,longitude,images) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
    val=(nextPage,name,category,description,address,transport,mrt,latitude,longitude,str(images),)
    mycursor=mydb.cursor()
    mycursor.execute(sql,val)
    mydb.commit()
mycursor.close()
    #print(images)

"""
MySQL 建立TABLE @ website 
use website;
CREATE TABLE taipei_attrations_website(
id bigint not null primary key auto_increment,
nextPage int not null,
name varchar(255) collate utf8mb4_unicode_ci null,
category varchar(255) collate utf8mb4_unicode_ci not null,
description varchar(255) collate utf8mb4_unicode_ci not null,
address varchar(255) collate utf8mb4_unicode_ci not null,
transport varchar(999) collate utf8mb4_unicode_ci not null,
mrt varchar(255) collate utf8mb4_unicode_ci, # prevent MRT=None
latitude double not null default 0,
longitude double not null default 0,
images varchar(9999) collate utf8mb4_unicode_ci not null,
time datetime not null default current_timestamp(),
INDEX(nextPage)
);

plugin='mysql_native_password' 

    sql="SELECT id,name,username FROM website.member WHERE username=%s"
    data=request.args.get("uname","")
    val=(data,)
    print(val)
    mycursor=mydb.cursor()
    mycursor.execute(sql,val)
    mydata=mycursor.fetchone()
    mycursor.close()
"""
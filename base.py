# -*- coding: utf-8 -*-
import sqlite3
import os
import json
from io import BytesIO

def db_read(column,table,nameid):
	conn = sqlite3.connect('db.sqlite')
	cursor = conn.cursor()
	cursor.execute("SELECT "+str(column)+" FROM "+str(table)+" WHERE id = "+str(nameid))
	results = cursor.fetchall()
	conn.close()
	str_files = results[0][0]
	return str_files

def db_list(column,table):
	conn = sqlite3.connect('db.sqlite')
	cursor = conn.cursor()
	cursor.execute("SELECT "+str(column)+" FROM "+str(table)+" ORDER BY id")
	results = cursor.fetchall()
	conn.close()
	str_files =[]
	for i in range(len(results)):
		file1 = results[i]
		for z in range(len(file1)):
			str_files.append(file1[z])
	return str_files

def db_write_list(column,table,files,nameid):
	print(len(files))
	file = ""
	for i in range(len(files)):
		if i ==  len(files)-1:
			z=""
		else:
			z=","
		file = file + files[i]+z
	file = "["+file+"]"
	db_write(column,table,file,nameid)

def db_read_list(column,table,nameid):
	files = db_read(column,table,nameid)
	print()
	files = files.replace(", ",",")
	str_file = list(str(files)+"]")
	real_list = []
	file = ""
	for i in range(len(str_file)):
		var = str_file[i].replace("[","")
		var = var.replace("'","")
		if var!=",":
			file = file+var
		else:
			real_list.append(file)
			file = ""

	return real_list

def db_write(column,table,insert,nameid):
	conn = sqlite3.connect('db.sqlite')
	cursor = conn.cursor()
	sql = "UPDATE "+str(table)+" SET "+str(column)+" = '"+str(insert)+"' WHERE id = "+str(nameid)
	cursor.execute(sql)
	conn.commit()

def db_users(table,nameid,step,state,path,basket):
	conn = sqlite3.connect('db.sqlite')
	cursor = conn.cursor()
	column = "id"
	files = db_list(column,table)
	sql = ("INSERT INTO "+str(table)+" VALUES("+str(nameid)+","+str(step)+","+str(state)+","+str(path)+","+str(basket)+")")
	cursor.execute(sql)
	conn.commit()


	

table = "users"
nameid = "1"
state = "1"
path = "123"
basket = "123"
column = "basket"
step = "0"

insert ="🥩"
place = "22"
chat_id = "123"

price = "1000"
how_many = "2"
name = "селедка🥩"


def db_new_user(chat_id):
    file=open(str(chat_id)+".sqlite","w")
    file.write("")
    file.close()
    conn = sqlite3.connect(str(chat_id)+'.sqlite')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE 'states' (key TEXT, value TEXT)")
    cursor.execute("CREATE TABLE 'basket' (name TEXT, price TEXT, how_many TEXT)")
    cursor.execute("CREATE TABLE 'path' (id TEXT, value TEXT)")
    conn.commit()

def state(chat_id,place,insert):
	conn = sqlite3.connect(str(chat_id)+'.sqlite')
	cursor = conn.cursor()
	table = "states"
	column = str(place)
	cursor = conn.cursor()
	cursor.execute("SELECT key FROM states WHERE key = '"+str(place)+"'")
	results = cursor.fetchall()
	if len(results) == 0:
		cursor.execute("INSERT INTO states VALUES('"+str(place)+"','"+str(insert)+"')")
	else:
		cursor.execute("UPDATE states SET value = '"+str(insert)+"' WHERE key = '"+str(place)+"'")
	conn.commit()
	conn.close()



def state_read(chat_id,place):
	conn = sqlite3.connect(str(chat_id)+'.sqlite')
	cursor = conn.cursor()
	cursor.execute("SELECT value FROM states WHERE key = "+str(place))
	results = cursor.fetchall()
	conn.close()
	str_files = results[0][0]
	return str_files	

def state_del(chat_id,place):
	conn = sqlite3.connect(str(chat_id)+'.sqlite')
	cursor = conn.cursor()
	cursor.execute('''DELETE FROM states WHERE key = ?''',(place,))
	conn.commit()
	conn.close()

def basket_add(chat_id,name,price,how_many):
	conn = sqlite3.connect(str(chat_id)+'.sqlite')
	cursor = conn.cursor()
	table = "states"
	column = str(place)
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM basket WHERE name = '"+str(name)+"'")
	results = cursor.fetchall()
	if len(results)==0:	
		cursor.execute("INSERT INTO basket VALUES('"+str(name)+"','"+str(price)+"','"+str(how_many)+"')")
	else:
		pass
	conn.commit()
	conn.close()

def basket_del(chat_id,name):
	conn = sqlite3.connect(str(chat_id)+'.sqlite')
	cursor = conn.cursor()
	cursor.execute('''DELETE FROM basket WHERE name = ?''',(name,))
	conn.commit()
	conn.close()

def basket_show(chat_id,i):
	conn = sqlite3.connect(str(chat_id)+'.sqlite')
	cursor = conn.cursor()
	cursor.execute("SELECT name FROM basket ORDER BY name")
	results = cursor.fetchall()
	conn.close()
	files = []
	for i in range(len(results)):
		print(results[i][0])
		


def db_img_write(data,nameid):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    binary = sqlite3.Binary(data)
    #cur.execute("INSERT INTO product (img) VALUES (?)", (binary,))
    #cur.execute("INSERT INTO img(id, img) VALUES (?, ?)", (nameid , binary))
    cur.execute("UPDATE product  SET img = (?)  WHERE id = (?)",(binary, nameid))
    con.commit()    
    con.rollback()
    con.close()

def db_img_read(nameid):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()    
    cur.execute("SELECT img FROM product WHERE id = (?)",(nameid))
    data = cur.fetchone()[0]  #проччтенное фото 
    con.close()
    return data



def db_read(column,table,nameid):
	conn = sqlite3.connect('db.sqlite')
	cursor = conn.cursor()
	cursor.execute("SELECT "+str(column)+" FROM "+str(table)+" WHERE id = "+str(nameid))
	results = cursor.fetchall()
	conn.close()
	str_files = results[0][0]
	return str_files





conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
files = os.listdir("product")
product = []
index = 0
for i in range(len(files)):
    files1 = os.listdir("product/"+files[i])
    name = files[i]
    cursor.execute("SELECT id FROM category WHERE name = (?)",(str(name),))
    results = cursor.fetchall()
    results = results[0][0]
    for z in range(len(files1)):
        index = int(index)+1
        product = files1[z].replace(".txt","")
        try:
            file = open("product_price/"+str(files1[z]),"r")
            price = file.read()
            file.close()
        except:
            price = "0"
        try:
            photo = open("img_product/"+str(product)+".jpg",'rb')
            data = photo.read()
            binary = sqlite3.Binary(data)
        except:
            binary = 'NULL'
            print(files1[z])

        cursor.execute("INSERT INTO product VALUES((?), (?), (?), '1' , (?), '1', (?))",(str(results),str(index),str(product),str(price),(binary)))
        #data.close()
        
        




conn.commit()
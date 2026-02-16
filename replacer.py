import os
import sqlite3

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT rev_uz FROM product")
results = cursor.fetchall()
for i in range(len(results)):
	res = results[i][0].replace("'","`") 
	res = res.replace('"','``')
	cursor.execute("UPDATE product SET rev_uz = '"+str(res)+"' WHERE id = '"+str(i+1)+"'")
conn.commit()
conn.close()
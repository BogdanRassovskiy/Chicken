import glob, os ,sys


file = open("name_bot.txt","r")
name_bot = file.read()
file.close()

os.chdir("..")
os.chdir("ITB")

file = open("last_index.txt","r")
data = file.read()
file.close()

file = open("last_index.txt","w")
file.write(str(int(data)+1))
file.close()

file = open("last_index.txt","r")
data = file.read()
file.close()

os.chdir("..")
os.chdir(name_bot)

file = open("last_index.txt","w")
file.write(data)
file.close()

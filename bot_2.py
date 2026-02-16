import glob, os ,sys
import shutil

file = open("name_bot.txt","r")
name_bot = file.read()
file.close()

file = open("last_index.txt","r")
index = file.read()
file.close()

os.chdir("..")
try:
	os.mkdir("ITB/not_del/"+str(name_bot))
except:
	pass
try:
    os.mkdir("ITB/partners/"+str(name_bot))
except:
    pass
try:
    os.mkdir("ITB/price_boss/"+str(name_bot))
except:
    pass
try:
    os.mkdir("ITB/not_del/"+str(name_bot))
except:
    pass
try:
    os.mkdir("ITB/active_del/"+str(name_bot))
except:
    pass
try:
    os.mkdir("ITB/done_del/"+str(name_bot))
except:
    pass
try:
    os.mkdir("ITB/adres/"+str(name_bot))
except:
    pass
try:
    os.mkdir("ITB/adres/"+str(name_bot)+"/filial")
except:
    pass
try:
    os.mkdir("ITB/order/"+str(name_bot))
except:
	pass

file = open(str(name_bot)+"/adres/longitude.txt","r")
lon = file.read()
file.close()

file = open(str(name_bot)+"/adres/latitude.txt","r")
lat = file.read()
file.close()

file = open("ITB/adres/"+str(name_bot)+"/filial/longitude.txt","w")
file.write(str(lon))
file.close()

file = open("ITB/adres/"+str(name_bot)+"/filial/latitude.txt","w")
file.write(str(lat))
file.close()


src = str(name_bot)+"/in time/"+str(index)+".txt"
dst = "ITB/not_del/"+str(name_bot)+"/"+str(index)+".txt"
shutil.copy(src,dst)

src = str(name_bot)+"/in time/"+str(index)+"lon.txt"
dst = "ITB/not_del/"+str(name_bot)+"/"+str(index)+"lon.txt"
shutil.copy(src,dst)

src = str(name_bot)+"/in time/"+str(index)+"lat.txt"
dst = "ITB/not_del/"+str(name_bot)+"/"+str(index)+"lat.txt"
shutil.copy(src,dst)

src = str(name_bot)+"/in time/"+str(index)+"time.txt"
dst = "ITB/not_del/"+str(name_bot)+"/"+str(index)+"time.txt"
shutil.copy(src,dst)

os.chdir(name_bot)

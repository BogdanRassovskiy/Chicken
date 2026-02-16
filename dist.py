import math
import sqlite3

def distance(Z,marsh_list):
    Ax = float(marsh_list[0][0])
    Ay = float(marsh_list[1][0])
    Bx = float(marsh_list[2][0])
    By = float(marsh_list[3][0])
    marsh_name = marsh_list[4][0]
    print(
        "Ax > "+str(Ax)
        +"\nAy > "+str(Ay)
        +"\nBx > "+str(Bx)
        +"\nBy > "+str(By)
        +"\n\nZ > "+str(Z)
        )
    if Ax < Bx:
        a1 = Ax
        b1 = Bx
        Bx = a1
        Ax = b1
    if Ay < By:
        a1 = Ay
        b1 = By
        By = a1
        Ay = b1
    first = []
    while Bx <= Ax:
        first.append(Bx)
        Bx = Bx + 1
    var = Ay - By
    try:
        koef = var/len(first)
    except:
        koef = 0
    second = []
    for i in range(len(first)):
        By = By + koef
        second.append(By)
    metr_list = []
    for i in range(len(first)):
        print("("+str(first[i])+","+str(second[i])+")")
        metr = dist(first[i],second[i],Z[0],Z[1])
        metr_list.append(metr)
    min_metr = min(metr_list)
    for i in range(len(metr_list)):
        if metr_list[i] == min_metr:
            this = [first[i],second[i],marsh_name]
            break
    print("\n\nshort way: ("+str(this[0])+","+str(this[1])+") name > "+str(this[2]))
    return this

def dist(x2,y2,x1,y1):
    X = (float(x1)-float(x2))
    X = X * X
    Y = (float(y1)-float(y2))
    Y = Y * Y
    S0 = X + Y 
    S = math.sqrt(S0)
    file = open("S.txt","w")
    file.write("\n"+str(S))
    file.close()
    file = open("S.txt","r")
    S = file.read()
    file.close()
    S = round(float(S),5)
    km = S *100
    km = round(float(km),3)
    m = float(km)*1000
    m = round(int(m),0)

    km = round(float(km),1)
    m = round(int(m),0)
    return m

def find_in_all(Z):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT A FROM locations ")
    A = cursor.fetchall()
    cursor.execute("SELECT B FROM locations ")
    B = cursor.fetchall()
    cursor.execute("SELECT C FROM locations ")
    C = cursor.fetchall()
    cursor.execute("SELECT D FROM locations ")
    D = cursor.fetchall()
    cursor.execute("SELECT E FROM locations ")
    E = cursor.fetchall()
    cursor.execute("SELECT F FROM locations ")
    F = cursor.fetchall()

    #A = [1,1,5,5,"A"]
    #B = [3,1,9,1,"B"]
    #C = [5,2,9,6,"C"]
    #D = [10,1,10,7,"D"]
    #E = [6,5,2,9,"E"]
    #F = [3,5,3,10,"F"]
    conn.close()
    marsh_list = [A,B,C,D,E,F]
    short_list = []
    short_name = []
    for i in range(len(marsh_list)):
        koor = distance(Z,marsh_list[i])
        short = dist(koor[0],koor[1],Z[0],Z[1])
        short_list.append(short)
        short_name.append(koor[2][0])
    for i in range(len(short_list)):
        if short_list[i] == min(short_list):
            print("short in all >> "+str(short_name[i]))    

Z = [69.199886,41.281516]
find_in_all(Z)
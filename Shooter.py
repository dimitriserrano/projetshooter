from os import name
from tkinter import *
import mysql.connector

######################################## Connexion a la bdd ###################################

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS Jeu2")

mydb.commit()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="Jeu2"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS player (name VARCHAR(255), speed FLOAT(10))")

mycursor.execute("CREATE TABLE IF NOT EXISTS score (name VARCHAR(255), point INTEGER(10))")

mydb.commit()

########################### Création de la fenêtre graphique #####################################

win = Tk() 
win.title("Shooter")
win.resizable(0, 0) 
canvas = Canvas(win, width=800, height=600,bg='black')
canvas.pack() 

########################### Classe joueur ################################

class Player :
    
    def __init__(self, name, score, vitesse, sprite, pv):
         
        self.name = name
        self.score = score
        self.vitesse = vitesse
        self.sprite = sprite
        self.pv = pv   

player1 = StringVar()
player2 = StringVar()

a=1
b=1
c=1
c2=1
d=0
e=0
end=0
vie1=0
vie2=0

inGame=0
inInstruction=0
inOption=0
inFirst=1
inAccueil=0

####################### controle ####################

def move_p1(event):
    if inGame == 1:
        if event.keysym == "z" and p1y0 > 0: 
            canvas.move(p1.sprite, 0, -30) 
            canvas.move(p1.pv, 0, -30)

        elif event.keysym == "s" and p1y1 < 600: 
            canvas.move(p1.sprite, 0, 30)
            canvas.move(p1.pv, 0, 30)


def move_p2(event):
    if inGame == 1:
        if event.keysym == "Up" and p2y0 > 0:
            canvas.move(p2.sprite, 0, -30)
            canvas.move(p2.pv, 0, -30)

        elif event.keysym == "Down" and p2y1 < 600:
            canvas.move(p2.sprite, 0, 30)
            canvas.move(p2.pv, 0, 30)

def move_ball(event):
    global a,c,d
    if d==0 and inGame == 1:
        a = 0
        c = 0

def move_ball2(event):  
    global b,c2,e
    if e==0 and inGame == 1:
        b = 0
        c2 = 0

######################### création du joueur dans la base de donnée ou récupération ####################

def Showbdd():

    n1exist = 0
    n2exist = 0

    mycursor = mydb.cursor()

    sqlFormule = "SELECT * FROM player"

    mycursor.execute(sqlFormule)

    for result in mycursor:

        if result[0] == p1.name:

            n1exist = 1
            p1.vitesse = result[1]

        if result[0] == p2.name:

            n2exist = 1
            p2.vitesse = result[1]

    if n1exist == 0:

        sqlFormule = "INSERT INTO player (name, speed) VALUES (%s, %s)"
        player = (p1.name, p1.vitesse)
        mycursor.execute(sqlFormule, player)
        mydb.commit()

    if n2exist == 0:

        sqlFormule = "INSERT INTO player (name, speed) VALUES (%s, %s)"
        player = (p2.name, p2.vitesse)
        mycursor.execute(sqlFormule, player)
        mydb.commit()
        
    mydb.commit()

################################### Toute première pages ###################################

def Page():
    global player1,player2, inFirst, entree, entree2
    if inFirst == 1:
        canvas.delete(ALL)

        canvas.create_text(300,100,text="Player 1 :",fill="white")

        entree = Entry(win, width=20, textvariable=player1)
        canvas.create_window(400, 100, window=entree)

        canvas.create_text(300,200,text="Player 2 :",fill="white")

        entree2 = Entry(win, width=20, textvariable=player2)
        canvas.create_window(400, 200, window=entree2)

        ButtonContinuer = Button(win, command=Transition, text = "OK")
        canvas.create_window(400, 300, window=ButtonContinuer)

def Transition():
    global inFirst, entree, entree2
    inFirst = 0
    entree.destroy()
    entree2.destroy()
    AccueilPage()

def AccueilPage():
    global player1, player2, inFirst, inAccueil
    inAccueil = 1
    if inAccueil == 1:
        canvas.delete(ALL)

        p1.name = player1.get()
        p2.name = player2.get()

        Showbdd()

        ButtonQuitter = Button(win, command = win.destroy, text = "Quitter",bg="red")
        canvas.create_window(400, 450, window=ButtonQuitter)

        ButtonQuitter = Button(win,command=InstructionPage, text = "Instructions")
        canvas.create_window(400, 400, window=ButtonQuitter)

        ButtonQuitter = Button(win, command=OptionPage,text = "Options")
        canvas.create_window(400, 350, window=ButtonQuitter)

        ButtonQuitter = Button(win, command=JeuPage, text = "Jouer")
        canvas.create_window(400, 300, window=ButtonQuitter)

        sqlFormule = "SELECT * FROM score ORDER BY point DESC LIMIT 3"

        mycursor.execute(sqlFormule)
        
        classementname = []
        classementpoint = []

        for r in mycursor:

            classementname.append(r[0])
            classementpoint.append(r[1])

        if len(classementname) == 3:   

            canvas.create_text(350,100,text=classementname[0],fill="white")
            canvas.create_text(350,150,text=classementname[1],fill="white")
            canvas.create_text(350,200,text=classementname[2],fill="white")
            canvas.create_text(450,100,text=classementpoint[0],fill="white")
            canvas.create_text(450,150,text=classementpoint[1],fill="white")
            canvas.create_text(450,200,text=classementpoint[2],fill="white")

        mydb.commit()


def InstructionPage():
    global inAccueil, inInstruction
    inInstruction = 1
    inAccueil = 0
    if inInstruction == 1:
        canvas.delete(ALL)
        ButtonPetitQuitter = Button(win, command = AccueilPage, text = "Retour")
        canvas.create_window(400, 550, window=ButtonPetitQuitter )

        canvas.create_text(400,100,text="Instructions",fill="white")
        canvas.create_text(400,200,text="Le but du jeu est de tuer l'autre joueur",fill="white")

def OptionPage():
    global xp1,xp2,inAccueil, inOption
    inAccueil = 0
    inOption = 1
    if inOption == 1:
        canvas.delete(ALL)

        ButtonPetitQuitter = Button(win, command = AccueilPage, text = "Retour")
        canvas.create_window(400, 550, window=ButtonPetitQuitter )

        ButtonPlus = Button(win, command = Increase, text = "+")
        canvas.create_window(350, 175, window=ButtonPlus )

        ButtonMoins = Button(win, command = Decrease, text = "-")
        canvas.create_window(350, 225, window=ButtonMoins)

        ButtonPlus2 = Button(win, command = Increase2, text = "+")
        canvas.create_window(350, 375, window=ButtonPlus2 )

        ButtonMoins2 = Button(win, command = Decrease2, text = "-")
        canvas.create_window(350, 425, window=ButtonMoins2)

        canvas.create_text(400,100,text="Options",fill="white")
        canvas.create_text(300,200,text="Joueur 1",fill="white")
        xp1=canvas.create_text(350,200,text=int(p1.vitesse * 10),fill="white")
        canvas.create_text(300,400,text="Joueur 2",fill="white")
        xp2=canvas.create_text(350,400,text=int(p2.vitesse * 10),fill="white")


def JeuPage():
    global inAccueil, inGame, end, vie1, vie2, a, b, c2, e
    canvas.delete(ALL)
    vie1 = 0
    vie2 = 0
    inAccueil = 0
    end = 0
    a=1
    b=1
    c2 = 1
    e = 0

    p1.sprite = canvas.create_rectangle(40, 285, 80, 315, fill='red') 

    p2.sprite = canvas.create_rectangle(720, 285, 760, 315, fill='blue') 

    p1.pv = canvas.create_rectangle(40, 275, 80, 265, fill='green')

    p2.pv = canvas.create_rectangle(720, 275, 760, 265, fill='green')


    inGame = 1

    jeu()

def jeu():
    global a,b,c,d,e,c2,vie1,vie2,p1x0, p1y0, p1x1, p1y1,p2x0, p2y0, p2x1, p2y1,ball,ball2, end
    if inGame == 1:
        if end==0:
            p1x0, p1y0, p1x1, p1y1 = canvas.coords(p1.sprite)
            p2x0, p2y0, p2x1, p2y1 = canvas.coords(p2.sprite)

            if a==0:
                d=1
                if c==0:
                    ball = canvas.create_oval(p1x1, p1y0 +10, p1x1 +10, p1y1-10, fill='white') 
                    c=1
                    if p1.score > 0:
                        p1.score = p1.score - 1 
                canvas.move(ball, p1.vitesse, 0)
                x0, y0, x1, y1 = canvas.coords(ball)
                if x1>=800:
                    a=1
                    d=0
                    canvas.delete(ball)
                if x1 >=720 and x1<= 760 :
                    if y1 <=p2y1 and y0 >= p2y0:
                        a=1
                        d=0
                        p1.score = p1.score + 100 - (p1.vitesse - p2.vitesse) * 100
                        if vie2 <2:
                            vie2+=1
                        else: vie2 = 0
                        canvas.delete(ball)
                        canvas.delete(p2.pv)
                        if vie2 == 1:
                            p1.score += 1
                            p2.pv = canvas.create_rectangle(p2x0, p2y0-10, p2x1-14, p2y1-50, fill='green')
                        if vie2 == 2:
                            p1.score += 1
                            p2.pv = canvas.create_rectangle(p2x0, p2y0-10, p2x1-28, p2y1-50, fill='green')
                        if vie2 == 0:
                            p1.score += 1
                            a = 1
                            GameOver()

            if b==0:
                e=1
                if c2==0:
                    ball2 = canvas.create_oval(p2x0-10, p2y0+10, p2x0, p2y1-10, fill='white') 
                    if p2.score > 0:
                        p2.score = p2.score - 1
                    c2=1
                canvas.move(ball2, - p2.vitesse, 0)
                x20, y20, x21, y21 = canvas.coords(ball2)
                if x21<=0:
                    b=1
                    e=0
                    canvas.delete(ball2)
                if x20 >=40 and x20<= 80 :
                    if y21 <=p1y1 and y20 >= p1y0:
                        b=1
                        e=0
                        p2.score = p2.score + 100 - (p2.vitesse - p1.vitesse) * 100
                        if vie1 <2:
                            vie1 += 1
                        else: vie1 = 0
                        canvas.delete(ball2)
                        canvas.delete(p1.pv)
                        if vie1 == 1:
                            p2.score += 1
                            p1.pv = canvas.create_rectangle(p1x0, p1y0-10, p1x1-14, p1y1-50, fill='green')
                        if vie1 == 2:
                            p2.score += 1
                            p1.pv =canvas.create_rectangle(p1x0, p1y0-10, p1x1-28, p1y1-50, fill='green')
                        if vie1 == 0:
                            p2.score += 1
                            b = 1
                            GameOver()
            win.after(1,jeu)

def GameOver():
    global inGame, inAccueil
    inGame=0
    canvas.delete(ALL)
    canvas.create_text(400,100,text="Score",fill="white")
    canvas.create_text(300,200,text="Joueur 1 : ",fill="white")
    canvas.create_text(500,200,text=p1.score,fill="white")
    canvas.create_text(300,300,text="Joueur 2 : ",fill="white")
    canvas.create_text(500,300,text=p2.score,fill="white")

    sqlFormule = "INSERT INTO score (name, point) VALUES (%s, %s)"
    scores = [(p1.name, p1.score),
                (p2.name, p2.score),]

    mycursor.executemany(sqlFormule, scores)

    mydb.commit()

    ButtonPetitQuitter = Button(win, command = AccueilPage, text = "Retour")
    canvas.create_window(400, 550, window=ButtonPetitQuitter )

    inAccueil = 1

def Increase():
    global xp1
    p1.vitesse = p1.vitesse + 0.1
    canvas.delete(xp1)
    xp1 = canvas.create_text(350,200,text=int(p1.vitesse * 10),fill="white")
    mycursor = mydb.cursor()

    sqlFormule = "UPDATE player SET speed = '"+str(p1.vitesse)+"' WHERE name = '"+str(p1.name)+"'"

    mycursor.execute(sqlFormule)

    mydb.commit()

def Decrease():
    global xp1
    p1.vitesse = p1.vitesse - 0.1
    canvas.delete(xp1)
    xp1 = canvas.create_text(350,200,text=int(p1.vitesse * 10),fill="white")
    mycursor = mydb.cursor()

    sqlFormule = "UPDATE player SET speed = '"+str(p1.vitesse)+"' WHERE name = '"+str(p1.name)+"'"

    mycursor.execute(sqlFormule)

    mydb.commit()

def Increase2():
    global xp2
    p2.vitesse = p2.vitesse + 0.1
    canvas.delete(xp2)
    xp2 = canvas.create_text(350,400,text=int(p2.vitesse * 10),fill="white")
    mycursor = mydb.cursor()

    sqlFormule = "UPDATE player SET speed = '"+str(p2.vitesse)+"' WHERE name = '"+str(p2.name)+"'"

    mycursor.execute(sqlFormule)

    mydb.commit()

def Decrease2():
    global xp2
    p2.vitesse = p2.vitesse - 0.1
    canvas.delete(xp2)
    xp2 = canvas.create_text(350,400,text=int(p2.vitesse * 10),fill="white")
    mycursor = mydb.cursor()

    sqlFormule = "UPDATE player SET speed = '"+str(p2.vitesse)+"' WHERE name = '"+str(p2.name)+"'"

    mycursor.execute(sqlFormule)

    mydb.commit()

p1 = Player("unknow", 0, 0.3, 0, 0)
p2 = Player("unknow", 0, 0.3, 0, 0)
Page()

canvas.bind_all("<KeyPress-z>", move_p1)
canvas.bind_all("<KeyPress-s>", move_p1)
canvas.bind_all("<KeyPress-Up>", move_p2)
canvas.bind_all("<KeyPress-Down>", move_p2)
canvas.bind_all("<KeyPress-a>", move_ball)
canvas.bind_all("<KeyPress-Right>", move_ball2)

win.mainloop()
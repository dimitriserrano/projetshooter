from tkinter import *
from math import *
import mysql.connector 

######################################## Connexion a la bdd ###################################

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS Game")

mydb.commit()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="Game"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS player (name VARCHAR(255), speed FLOAT(10))")

mycursor.execute("CREATE TABLE IF NOT EXISTS score (name VARCHAR(255), point INTEGER(10))")

mydb.commit()

######################################## Création de la fenêtre ###################################

win = Tk()
win.title("Shooter")
win.resizable(0, 0)
canvas = Canvas(win, width=800, height=600,bg='white')
canvas.pack()

##################################
#                                #
#                                #
#          Classe joueur         #
#                                #
#                                #
##################################

class Player:
    
    def __init__(self, name, score, vitesse, sprite):
         
        self.name = name
        self.score = score
        self.vitesse = vitesse
        self.sprite = sprite
        self.pv = []
        self.vie = 3

    def moveUp(self):
        canvas.move(self.sprite, 0, -20)

    def moveDown(self):
        canvas.move(self.sprite, 0, 20)

##################################
#                                #
#                                #
#          Classe balle          #
#                                #
#                                #
##################################

class Balle:
    def __init__(self,x,y,up,inf):
        self.x = x
        self.y = y
        self.up = up
        self.inf = inf
        self.entir = True

# Méthodes qui simule la visée du tir du joueur 2 grâce a la fonction demi-cercle

    def moveAroundLeft(self,other):
        if self.entir == True:
            if self.x<-98:
                inc = 0.02
            else: inc = 0.5
            if self.up == True and self.inf == True:
                canvas.delete(self.shape2)
                self.x+=inc
                self.y = -sqrt(10000-self.x**2)
                if self.x >= -70:
                    self.inf = False
                else : self.shape2 = canvas.create_oval(self.x+canvas.coords(other.sprite)[2],self.y+canvas.coords(other.sprite)[1]+10,self.x+canvas.coords(other.sprite)[2]+10,self.y+canvas.coords(other.sprite)[3]-10,fill="yellow")

            if self.up == True and self.inf == False:
                canvas.delete(self.shape2)
                self.x-=inc
                self.y = -sqrt(10000-self.x**2)
                if self.x < -99.98:
                    self.up = False
                else:self.shape2 = canvas.create_oval(self.x+canvas.coords(other.sprite)[2],self.y+canvas.coords(other.sprite)[1]+10,self.x+canvas.coords(other.sprite)[2]+10,self.y+canvas.coords(other.sprite)[3]-10,fill="yellow")

            if self.up == False and self.inf == False:
                canvas.delete(self.shape2)
                self.x+=inc
                self.y = sqrt(10000-self.x**2)
                if self.x >= -70:  
                    self.inf = True
                else:self.shape2 = canvas.create_oval(self.x+canvas.coords(other.sprite)[2],self.y+canvas.coords(other.sprite)[1]+10,self.x+canvas.coords(other.sprite)[2]+10,self.y+canvas.coords(other.sprite)[3]-10,fill="yellow")

            if self.up == False and self.inf == True:
                canvas.delete(self.shape2)
                self.x-=inc
                self.y = sqrt(10000-self.x**2)
                if self.x < -99.98:    
                    self.up = True
                else:self.shape2 = canvas.create_oval(self.x+canvas.coords(other.sprite)[2],self.y+canvas.coords(other.sprite)[1]+10,self.x+canvas.coords(other.sprite)[2]+10,self.y+canvas.coords(other.sprite)[3]-10,fill="yellow")

# Méthodes qui simule la visée du tir du joueur 1 grâce a la fonction demi-cercle

    def moveAroundRight(self,other):
        if self.entir == True:
            if self.x>98:
                inc = 0.02
            else: inc = 0.5
            if self.up == True and self.inf == True:
                canvas.delete(self.shape)
                self.x-=inc
                self.y = -sqrt(10000-self.x**2)
                if self.x <= 70:    
                    self.inf = False
                else : self.shape = canvas.create_oval(self.x+canvas.coords(other.sprite)[2]-50,self.y+canvas.coords(other.sprite)[1]+10,self.x+canvas.coords(other.sprite)[2]-40,self.y+canvas.coords(other.sprite)[3]-10,fill="yellow")

            if self.up == True and self.inf == False:
                canvas.delete(self.shape)
                self.x+=inc
                self.y = -sqrt(10000-self.x**2)
                if self.x >= 99.98:
                    self.up = False
                else:self.shape = canvas.create_oval(self.x+canvas.coords(other.sprite)[2]-50,self.y+canvas.coords(other.sprite)[1]+10,self.x+canvas.coords(other.sprite)[2]-40,self.y+canvas.coords(other.sprite)[3]-10,fill="yellow")

            if self.up == False and self.inf == False:
                canvas.delete(self.shape)
                self.x-=inc
                self.y = sqrt(10000-self.x**2)
                if self.x <= 70:  
                    self.inf = True
                else:self.shape = canvas.create_oval(self.x+canvas.coords(other.sprite)[2]-50,self.y+canvas.coords(other.sprite)[1]+10,self.x+canvas.coords(other.sprite)[2]-40,self.y+canvas.coords(other.sprite)[3]-10,fill="yellow")

            if self.up == False and self.inf == True:
                canvas.delete(self.shape)
                self.x+=inc
                self.y = sqrt(10000-self.x**2)
                if self.x > 99.98:    
                    self.up = True
                else:self.shape = canvas.create_oval(self.x+canvas.coords(other.sprite)[2]-50,self.y+canvas.coords(other.sprite)[1]+10,self.x+canvas.coords(other.sprite)[2]-40,self.y+canvas.coords(other.sprite)[3]-10,fill="yellow")

# Méthode qui permet de connaitre le vecteur de direction entre la balle et le joueur 

    def vecteur(self,other):
        vx = ((canvas.coords(self.shape)[0] + canvas.coords(self.shape)[2]) / 2) - ((canvas.coords(other.sprite)[0] + canvas.coords(other.sprite)[2]) / 2)
        vy = ((canvas.coords(self.shape)[1] + canvas.coords(self.shape)[3]) / 2) - ((canvas.coords(other.sprite)[1] + canvas.coords(other.sprite)[3]) / 2)
        self.vx = vx / other.vitesse
        self.vy = vy / other.vitesse

    def vecteur2(self,other):
        vx = ((canvas.coords(self.shape2)[0] + canvas.coords(self.shape2)[2]) / 2) - ((canvas.coords(other.sprite)[0] + canvas.coords(other.sprite)[2]) / 2)
        vy = ((canvas.coords(self.shape2)[1] + canvas.coords(self.shape2)[3]) / 2) - ((canvas.coords(other.sprite)[1] + canvas.coords(other.sprite)[3]) / 2)
        self.vx = vx / other.vitesse
        self.vy = vy / other.vitesse

# Méthode qui vérouille la balle suite a l'appuie sur le bouton correspondant et appelle le calcul du vecteur 

    def preparationTir(self,other):
        self.entir = False
        self.vecteur(other)

    def preparationTir2(self,other):
        self.entir = False
        self.vecteur2(other)

# Méthode qui déplace la balle selon le vecteur direction calculer au moment du tir

    def tir(self):
        canvas.move(self.shape,self.vx,self.vy)

    def tir2(self):
        canvas.move(self.shape2,self.vx,self.vy)

# Méthode qui gère les rebond contre les murs horizontaux 

    def collisionWall(self):
        if canvas.coords(self.shape)[1] <= 0:
            self.vy = -self.vy
        if canvas.coords(self.shape)[1] >= 600:
            self.vy = -self.vy

    def collisionWall2(self):
        if canvas.coords(self.shape2)[1] <= 0:
            self.vy = -self.vy
        if canvas.coords(self.shape2)[1] >= 600:
            self.vy = -self.vy

# Méthode qui vérifie si le tir a toucher l'adversaire

    def touch(self,other,other2):
        if canvas.coords(self.shape)[2] > canvas.coords(other.sprite)[0] and canvas.coords(self.shape)[0] < canvas.coords(other.sprite)[2] :
            if canvas.coords(self.shape)[3] > canvas.coords(other.sprite)[1] and canvas.coords(self.shape)[1] < canvas.coords(other.sprite)[3]:
                if other.vie == 1 :
                    other2.score += 50
                    self.entir = True
                    finGame()
                else:
                    other.vie -= 1
                    other2.score += 50
                    canvas.delete(self.shape)
                    canvas.delete(other.pv[len(other.pv)-1])
                    other.pv.pop()
                    self.entir = True
                

# Méthode qui vérifie si le tir a toucher le mur derriere le joueur adverse

    def miss(self,other):
        if canvas.coords(self.shape)[2] > 800:
            other.score -= 5
            canvas.delete(self.shape)
            self.entir = True

    def touch2(self,other,other2):
        if canvas.coords(self.shape2)[0] < canvas.coords(other.sprite)[2] and canvas.coords(self.shape2)[2] > canvas.coords(other.sprite)[0]:
            if canvas.coords(self.shape2)[3] > canvas.coords(other.sprite)[1] and canvas.coords(self.shape2)[1] < canvas.coords(other.sprite)[3]:
                if other.vie == 1 :
                    other2.score += 50
                    self.entir = True
                    finGame()
                else: 
                    other.vie -= 1
                    other2.score += 50
                    canvas.delete(self.shape2)
                    canvas.delete(other.pv[len(other.pv)-1])
                    other.pv.pop()
                    self.entir = True

    def miss2(self,other):
        if canvas.coords(self.shape2)[0] < 0:
            other.score -= 5
            canvas.delete(self.shape2)
            self.entir = True


player1 = Player("unknow", 0, 20, 0)
player2 = Player("unknow", 0, 20, 0)
balle1 = Balle(100,-sqrt(100000-100**2),True,True)
balle2 = Balle(-100,-sqrt(100000+100**2),True,True)
fond = PhotoImage(file = 'Fond.png')
fond2 = PhotoImage(file = 'fond2.png')
fondmini = PhotoImage(file = 'Fondmini.png')
fond2mini = PhotoImage(file = 'fond2mini.png')
im = PhotoImage(file = 'Heart.png')
rectanglescore = PhotoImage(file = 'rectanglescore.png')
petitrectangle = PhotoImage(file = 'petitrectangle.png')
grandrectangle = PhotoImage(file = 'grandrectangle.png')
gameover = PhotoImage(file = 'gameover.png')
nameplayer1 = StringVar()
nameplayer2 = StringVar()
fondlayout = 1

inPage = True
inAccueil = False
inGame = False
inMenu = False
inGameOver = False

######################### création du joueur dans la base de donnée ou récupération ####################

def Showbdd():

    n1exist = 0
    n2exist = 0

    mycursor = mydb.cursor()

    sqlFormule = "SELECT * FROM player"

    mycursor.execute(sqlFormule)

    for result in mycursor:

        if result[0] == player1.name:

            n1exist = 1
            player1.vitesse = result[1]

        if result[0] == player2.name:

            n2exist = 1
            player2.vitesse = result[1]

    if n1exist == 0:

        sqlFormule = "INSERT INTO player (name, speed) VALUES (%s, %s)"
        player = (player1.name, player1.vitesse)
        mycursor.execute(sqlFormule, player)
        mydb.commit()

    if n2exist == 0:

        sqlFormule = "INSERT INTO player (name, speed) VALUES (%s, %s)"
        player = (player2.name, player2.vitesse)
        mycursor.execute(sqlFormule, player)
        mydb.commit()
        
    mydb.commit()

def viserPlayer2():
    if inGame == True:
        balle2.moveAroundLeft(player2)
        win.after(10,viserPlayer2)

def viserPlayer1():
    if inGame == True:
        balle1.moveAroundRight(player1)
        win.after(10,viserPlayer1)

def deplacementBalle1():
    if balle1.entir == False:
        balle1.tir()
        balle1.collisionWall()
        balle1.touch(player2, player1)
        if balle1.entir == False:
            balle1.miss(player1)
        win.after(10,deplacementBalle1)

def deplacementBalle2():
    if balle2.entir == False:
        balle2.tir2()
        balle2.collisionWall2()
        balle2.touch2(player1, player2)
        if balle2.entir == False:
            balle2.miss2(player2)
        win.after(10,deplacementBalle2)

def prepa(event):
    if balle1.entir == True and inGame == True:
        balle1.preparationTir(player1)
        deplacementBalle1()

def prepa2(event):
    if balle2.entir == True and inGame == True:
        balle2.preparationTir2(player2)
        deplacementBalle2()

def moveUpPlayer1(event):
    if canvas.coords(player1.sprite)[1] > 100:
        player1.moveUp()

def moveDownPlayer1(event):
    if canvas.coords(player1.sprite)[3] < 500:
        player1.moveDown()

def moveUpPlayer2(event):
    if canvas.coords(player2.sprite)[1] > 100:
        player2.moveUp()

def moveDownPlayer2(event):
    if canvas.coords(player2.sprite)[3] < 500:
        player2.moveDown()

def Page():
    global nameplayer1,nameplayer2, entree, entree2, inPage
    if inPage == True:
        canvas.delete(ALL)
        if fondlayout == 1:
            canvas.create_image(400, 300,image=fond)
        else : 
            canvas.create_image(400, 300,image=fond2)
        canvas.create_text(300,100,text="Player 1 :",fill="white")

        entree = Entry(win, width=20, textvariable=nameplayer1)
        canvas.create_window(400, 100, window=entree)

        canvas.create_text(300,200,text="Player 2 :",fill="white")

        entree2 = Entry(win, width=20, textvariable=nameplayer2)
        canvas.create_window(400, 200, window=entree2)

        ButtonContinuer = Button(win, command=Transition, text = "OK")
        canvas.create_window(400, 300, window=ButtonContinuer)

def Transition():
    global entree, entree2, inPage, inAccueil
    canvas.delete(ALL)
    entree.destroy()
    entree2.destroy()
    inPage = False
    inAccueil = True
    AccueilPage()

def AccueilPage():
    global nameplayer1, nameplayer2, inFirst, inAccueil
    if inAccueil == True:
        canvas.delete(ALL)
        if fondlayout == 1:
            canvas.create_image(400, 300,image=fond)
        else : 
            canvas.create_image(400, 300,image=fond2)

        player1.name = nameplayer1.get()
        player2.name = nameplayer2.get()

        Showbdd()

        canvas.create_image(400, 150,image=petitrectangle)

        ButtonQuitter = Button(win, command = win.destroy, text = "Quitter",bg="red")
        canvas.create_window(400, 550, window=ButtonQuitter)

        ButtonQuitter = Button(win,command=ViePage, text = "Vie")
        canvas.create_window(400, 500, window=ButtonQuitter)

        ButtonQuitter = Button(win,command=LayoutPage, text = "Layout")
        canvas.create_window(400, 450, window=ButtonQuitter)

        ButtonQuitter = Button(win,command=InstructionPage, text = "Instructions")
        canvas.create_window(400, 400, window=ButtonQuitter)

        ButtonQuitter = Button(win, command=OptionPage,text = "Options")
        canvas.create_window(400, 350, window=ButtonQuitter)

        ButtonQuitter = Button(win, command=goGame, text = "Jouer")
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
    canvas.delete(ALL)
    if fondlayout == 1:
        canvas.create_image(400, 300,image=fond)
    else : 
        canvas.create_image(400, 300,image=fond2)
    canvas.create_image(400, 250,image=grandrectangle)
    ButtonPetitQuitter = Button(win, command = AccueilPage, text = "Retour")
    canvas.create_window(400, 550, window=ButtonPetitQuitter )

    canvas.create_text(400,100,text="Instructions",fill="white")
    canvas.create_text(400,200,text="Le but du jeu est de tuer l'autre joueur",fill="white")

def LayoutPage():
    canvas.delete(ALL)
    if fondlayout == 1:
        canvas.create_image(400, 300,image=fond)
    else : 
        canvas.create_image(400, 300,image=fond2)
    ButtonPetitQuitter = Button(win, command = AccueilPage, text = "Retour")
    canvas.create_window(400, 550, window=ButtonPetitQuitter )

    canvas.create_text(400,100,text="Layout",fill="white")
    canvas.create_image(200, 300,image=fondmini)
    canvas.create_image(600, 300,image=fond2mini)
    Buttonchoix = Button(win, command = choix1, text = "choisir")
    canvas.create_window(200, 400, window=Buttonchoix )
    Buttonchoix = Button(win, command = choix2, text = "choisir")
    canvas.create_window(600, 400, window=Buttonchoix )

def choix1():
    global fondlayout
    fondlayout = 1

def choix2():
    global fondlayout
    fondlayout = 2

def OptionPage():
    global displayspeed, displayspeed2
    canvas.delete(ALL)
    if fondlayout == 1:
        canvas.create_image(400, 300,image=fond)
    else : 
        canvas.create_image(400, 300,image=fond2)

    canvas.create_image(400, 250,image=grandrectangle)

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
    canvas.create_text(300,200,text=player1.name,fill="white")
    displayspeed=canvas.create_text(350,200,text=int(-player1.vitesse),fill="white")
    canvas.create_text(300,400,text=player2.name,fill="white")
    displayspeed2=canvas.create_text(350,400,text=int(-player2.vitesse),fill="white")

def goGame():
    global inAccueil,inGame
    canvas.delete(ALL)
    inGame = True
    inAccueil = False
    game()

def game():
    global inGame
    if inGame == True:
        if fondlayout == 1:
            canvas.create_image(400, 300,image=fond)
        else : 
            canvas.create_image(400, 300,image=fond2)
        player2.sprite = canvas.create_rectangle(720, 285, 760, 315, fill='red') 
        player1.sprite = canvas.create_rectangle(40, 285, 80, 315, fill='blue') 
        balle1.shape = canvas.create_oval(balle1.x+canvas.coords(player1.sprite)[2]-50,balle1.y+canvas.coords(player1.sprite)[1]+10,balle1.x+canvas.coords(player1.sprite)[2]-40,balle1.y+canvas.coords(player1.sprite)[3]-10,fill="yellow")
        balle2.shape2 = canvas.create_oval(balle2.x+canvas.coords(player2.sprite)[2],balle2.y+canvas.coords(player2.sprite)[1]+10,balle2.x+canvas.coords(player2.sprite)[2]+10,balle2.y+canvas.coords(player2.sprite)[3]-10,fill="yellow")
        i=0
        j=0
        player1.score = player1.vitesse
        player2.score = player2.vitesse
        while i < player1.vie:
            player1.pv.append(canvas.create_image(50+j, 50,image=im))
            i+=1
            j+=50
        i=0
        j=0
        while i < player2.vie:
            player2.pv.append(canvas.create_image(750-j, 50,image=im))
            i+=1
            j+=50
        viserPlayer2()
        viserPlayer1()

def finGame():
    global inGame, inGameOver
    inGame = False
    inGameOver = True
    player1.pv.clear()
    player2.pv.clear()
    player1.vie = 3
    player2.vie = 3
    gameOver()

def gameOver():
    global inGameOver, inAccueil
    if inGameOver == True:
        canvas.delete(ALL)
        if fondlayout == 1:
            canvas.create_image(400, 300,image=fond)
        else : 
            canvas.create_image(400, 300,image=fond2)
        canvas.create_image(400,200,image=rectanglescore)
        canvas.create_text(400,100,text="Score",fill="white")
        canvas.create_text(300,200,text=player1.name,fill="white")
        canvas.create_text(500,200,text=player1.score,fill="white")
        canvas.create_text(300,300,text=player2.name,fill="white")
        canvas.create_text(500,300,text=player2.score,fill="white")
        canvas.create_image(400,450,image=gameover)

        sqlFormule = "INSERT INTO score (name, point) VALUES (%s, %s)"
        scores = [(player1.name, player1.score),
                    (player2.name, player2.score),]

        mycursor.executemany(sqlFormule, scores)

        mydb.commit()

        inAccueil = True

        ButtonPetitQuitter = Button(win, command = AccueilPage, text = "Retour")
        canvas.create_window(400, 550, window=ButtonPetitQuitter )

def ViePage():
    global displayvie, displayvie2
    canvas.delete(ALL)
    if fondlayout == 1:
        canvas.create_image(400, 300,image=fond)
    else : 
        canvas.create_image(400, 300,image=fond2)
    canvas.create_image(400, 250,image=grandrectangle)

    ButtonPlus = Button(win, command = Increasevie, text = "+")
    canvas.create_window(350, 175, window=ButtonPlus )

    ButtonMoins = Button(win, command = Decreasevie, text = "-")
    canvas.create_window(350, 225, window=ButtonMoins)

    ButtonPlus2 = Button(win, command = Increasevie2, text = "+")
    canvas.create_window(350, 375, window=ButtonPlus2 )

    ButtonMoins2 = Button(win, command = Decreasevie2, text = "-")
    canvas.create_window(350, 425, window=ButtonMoins2)

    ButtonPetitQuitter = Button(win, command = AccueilPage, text = "Retour")
    canvas.create_window(400, 550, window=ButtonPetitQuitter )
    canvas.create_text(300,200,text=player1.name,fill="white")
    displayvie=canvas.create_text(350,200,text=int(player1.vie),fill="white")
    canvas.create_text(300,400,text=player2.name,fill="white")
    displayvie2=canvas.create_text(350,400,text=int(player2.vie),fill="white")
    canvas.create_text(400,100,text="Vie",fill="white")
    
def Increasevie():
    global displayvie
    if player1.vie < 5:
        player1.vie += 1
        canvas.delete(displayvie)
        displayvie = canvas.create_text(350,200,text=int(player1.vie),fill="white")
        

def Decreasevie():
    global displayvie
    if player1.vie > 1:
        player1.vie -= 1
        canvas.delete(displayvie)
        displayvie = canvas.create_text(350,200,text=int(player1.vie),fill="white")
        

def Increasevie2():
    global displayvie2
    if player2.vie < 5:
        player2.vie += 1
        canvas.delete(displayvie2)
        displayvie2 = canvas.create_text(350,400,text=int(player2.vie),fill="white")
        

def Decreasevie2():
    global displayvie2
    if player2.vie > 1:
        player2.vie -= 1
        canvas.delete(displayvie2)
        displayvie2 = canvas.create_text(350,400,text=int(player2.vie),fill="white")
        

def Increase():
    global displayspeed
    if player1.vitesse > 10:
        player1.vitesse = player1.vitesse - 5
        canvas.delete(displayspeed)
        displayspeed = canvas.create_text(350,200,text=int(-player1.vitesse),fill="white")
        mycursor = mydb.cursor()

        sqlFormule = "UPDATE player SET speed = '"+str(player1.vitesse)+"' WHERE name = '"+str(player1.name)+"'"

        mycursor.execute(sqlFormule)

        mydb.commit()

def Decrease():
    global displayspeed
    if player1.vitesse < 50:
        player1.vitesse = player1.vitesse + 5
        canvas.delete(displayspeed)
        displayspeed = canvas.create_text(350,200,text=int(-player1.vitesse),fill="white")
        mycursor = mydb.cursor()

        sqlFormule = "UPDATE player SET speed = '"+str(player1.vitesse)+"' WHERE name = '"+str(player1.name)+"'"

        mycursor.execute(sqlFormule)

        mydb.commit()

def Increase2():
    global displayspeed2
    if player2.vitesse > 10:
        player2.vitesse = player2.vitesse - 5
        canvas.delete(displayspeed2)
        displayspeed2 = canvas.create_text(350,400,text=int(-player2.vitesse),fill="white")
        mycursor = mydb.cursor()

        sqlFormule = "UPDATE player SET speed = '"+str(player2.vitesse)+"' WHERE name = '"+str(player2.name)+"'"

        mycursor.execute(sqlFormule)

        mydb.commit()

def Decrease2():
    global displayspeed2
    if player2.vitesse < 50:
        player2.vitesse = player2.vitesse + 5
        canvas.delete(displayspeed2)
        displayspeed2 = canvas.create_text(350,400,text=int(-player2.vitesse),fill="white")
        mycursor = mydb.cursor()

        sqlFormule = "UPDATE player SET speed = '"+str(player2.vitesse)+"' WHERE name = '"+str(player2.name)+"'"

        mycursor.execute(sqlFormule)

        mydb.commit()

Page()

canvas.bind_all("<KeyPress-a>", prepa)
canvas.bind_all("<KeyPress-z>", prepa2)
canvas.bind_all("<KeyPress-Up>", moveUpPlayer1)
canvas.bind_all("<KeyPress-Down>", moveDownPlayer1)
canvas.bind_all("<KeyPress-s>", moveUpPlayer2)
canvas.bind_all("<KeyPress-w>", moveDownPlayer2)

win.mainloop()
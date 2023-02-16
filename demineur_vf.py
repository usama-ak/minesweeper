#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 
"""
----------------------------------------------------------------------------
 Created By  : AKHTAR Usama
 Created Date: Thur Dec 29 2022
 --------------------------------------------------------------------------- 
"""

import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox

"""La classe Grille va créer la grille de jeu lors du lancement du jeu et régulera la progression du jeu,
comme l'inspection des résultats gagnant/perdant, ainsi que découvrir le jeu lors du clic sur une case vide"""
class Grille:
    def __init__(self,n,k,frame):
        self.largeur = n
        self.longueur = n
        self.matrice = [[0 for u in range(n)] for v in range(n)]
        self.bombe = 0
        self.bombemax = k
        self.frame=frame
        self.fillmatrix()

    """Remplissage de la matrice de jeu avec des X (bombes) placés au hasard et annotation des cases autour des bombes : on ajoute +1 
    dans les cases autour de chaque bombes"""
    def fillmatrix(self):
        while self.bombe < self.bombemax :
            x = random.randint(0,self.largeur-1)
            y = random.randint(0,self.largeur-1)
            if self.matrice[y][x] != "X":
                self.matrice[y][x] = "X"
                if (x>=0 and x <=self.largeur-2) and (y>=0 and y<=self.largeur-1):
                    if self.matrice[y][x+1] != "X":
                        self.matrice[y][x+1] += 1 #centre droit
            
                if (x>=1 and x<=self.largeur-1) and (y>=0 and y<=self.largeur-1):
                    if self.matrice[y][x-1] != "X":
                        self.matrice[y][x-1] += 1 #centre gauche

                if (x>=1 and x <=self.largeur-1) and (y>=1 and y<=self.largeur-1):
                    if self.matrice[y-1][x-1] != "X":
                        self.matrice[y-1][x-1] += 1 #haut gauche

                if (x>=0 and x <=self.largeur-1) and (y>=1 and y<=self.largeur-1):
                    if self.matrice[y-1][x] != "X":
                        self.matrice[y-1][x] += 1 #haut centre

                if (x>=0 and x <=self.largeur-2) and (y>=1 and y<=self.largeur-1):
                    if self.matrice[y-1][x+1] != "X":
                        self.matrice[y-1][x+1] += 1 #haut droit

                if (x>=0 and x <=self.largeur-2) and (y>=0 and y<=self.largeur-2):
                    if self.matrice[y+1][x+1] != "X":
                        self.matrice[y+1][x+1] += 1 #bas droit

                if (x>=0 and x <=self.largeur-1) and (y>=0 and y<=self.largeur-2):
                    if self.matrice[y+1][x] != "X":
                        self.matrice[y+1][x] += 1 #bas centre

                if (x>=1 and x <=self.largeur-1) and (y>=0 and y<=self.largeur-2):
                    if self.matrice[y+1][x-1] != "X":
                        self.matrice[y+1][x-1] += 1 #bas gauche
                self.bombe+=1

    """Lors d'un clic sur une case vide, la méthode montre les cases adjacentes jusqu'à tomber des cases avec des chiffres"""
    def decouvrir(self,bouton,x,y):
        widgets = self.frame.grid_slaves()
        nw = [widgets[i:i+self.longueur] for i in range(0, len(widgets), self.largeur)]
        dbx=x-1
        fnx=x+1
        dby=y-1
        fny=y+1
        if dbx < 0:
            dbx = 0
        if dby < 0:
            dby = 0
        if fnx >= self.largeur-1:
            fnx = self.largeur-1
        if fny >= self.largeur-1:
            fny = self.largeur-1
        i=0
        j=0
        for i in range(dbx,fnx+1):
            for j in range(dby,fny+1):
                if nw[self.largeur-i-1][self.largeur-j-1]["text"]=="0":
                    nw[self.largeur-i-1][self.largeur-j-1].config(bg="white",state=DISABLED, text="")
                    nw[self.largeur-i-1][self.largeur-j-1].unbind('<Button-1>')
                    self.decouvrir(nw[self.largeur-i-1][self.largeur-j-1],x=i,y=j)
                elif nw[self.largeur-i-1][self.largeur-j-1]["text"]=="":
                    pass
                else:
                    nw[self.largeur-i-1][self.largeur-j-1].config(bg="white",state=DISABLED)
                    nw[self.largeur-i-1][self.largeur-j-1].unbind('<Button-1>')
    
    """Méthode pour vérifier si le joueur à gagné, c'est-à-dire que les cases avec des bombes (X) sont coloré en vert après clic droit et 
    que le reste des cases sont tous découvert evec un clic gauche, ainsi que montrer la fenetre final où tout est montré au joueur"""
    def checkwin(self):
        widgets = self.frame.grid_slaves()
        subset = [i for i in widgets if i["text"]=="X"]
        subset2 = [i for i in widgets if i["text"]!="X"]
        """Si tous les boutons qui cachent des bombes sont marqués en vert et tous les boutons qui ne sont pas des bombes sont désacivés 
        suite a un clic droit"""
        if all(ele["bg"]=="green" for ele in subset) == True and all(ele["state"]==DISABLED for ele in subset2) == True :
            for widget in self.frame.winfo_children():
                widget.configure(state='disable')
                widget.unbind('<Button-1>')
                if widget["text"]=="0":
                    widget.config(bg="white",text="")
                elif widget["text"]=="X":
                    widget.config(bg="green",fg="black")
                else:
                    widget.config(bg="white",fg="black")
            tk.messagebox.showinfo(message="You Win !")
        else:   pass




class Game:
    def __init__(self):
        """Creation de la fenetre de jeu"""
        self.fenetre = tk.Tk()
        self.fenetre.title("Démineur")
        self.fenetre.geometry("400x500")
        self.grille=None
        
        quitbutton = Button(self.fenetre, text= "Quitter", bg= "white", command= self.fenetre.destroy)
        quitbutton.place(x=0, y=0)
        newgamebutton = Button(self.fenetre, text= "New Game",bg= "white",command=self.createboard)
        newgamebutton.place(x=0, y=25)

        frame = tk.LabelFrame(self.fenetre,text="Choose wisely")
        frame.pack(pady=10, anchor="n")
        self.d = IntVar()
        Radiobutton(frame, text='Easy', variable=self.d, value=8 ).grid(row=0, column=1)
        Radiobutton(frame, text="Normal", variable=self.d, value=12 ).grid(row=0, column=2)
        Radiobutton(frame, text="Hard", variable=self.d, value=16 ).grid(row=0, column=3)
        self.frame2 = Frame(self.fenetre)
        self.frame2.pack()
        self.frame3 = Frame(self.fenetre)
        self.frame3.pack()
        self.condition = Label(self.frame3)
        self.condition.pack()

    """Methode pour créer une grille de jeu en fonction des paramètres donnée et de créer les cellules """
    def createboard(self):
        """création de la grille de jeu"""
        if self.d.get()==8 :
            self.grille = Grille(n=self.d.get(),k=3, frame=self.frame2)
            self.condition.config( text=f"Nombre de bombes à trouver : {self.grille.bombemax}")
        elif self.d.get()==12 :
            self.grille =Grille(self.d.get(),14, frame=self.frame2)
            self.condition.config( text=f"Nombre de bombes à trouver : {self.grille.bombemax}")
        elif self.d.get()==16 :
            self.grille =Grille(self.d.get(),51,frame=self.frame2)
            self.condition.config( text=f"Nombre de bombes à trouver : {self.grille.bombemax}")

        """Vider la fenetre pour mettre en place le jeu"""    
        for widget in self.frame2.winfo_children():
            widget.destroy()
        
        """creation des objets cellules qui vont s'afficher dans la fenetre"""
        for x in range(0, self.d.get()):
            for y in range(0, self.d.get()):
                v=self.grille.matrice[x][y]
                Cellule(x, y,self.grille, self.frame2,value=str(v), state=NORMAL, bg= "grey",text="", fg="grey", labelbombe=self.condition)

    def play(self):
        self.fenetre.mainloop()

"""La classe Cellule va permettre de créer des objets cellules qui vont s'afficher sous forme de boutons"""
class Cellule:  
    def __init__(self, x, y,grille,frame,value,state,bg,text,fg, labelbombe):  
        self.x = x  
        self.y = y
        self.value = value
        self.grille = grille
        self.frame=frame
        self.labelbombe=labelbombe  
        self.button = tk.Button(self.frame, text=value, width=2, height=1, state=state, bg=bg, fg=fg)  
        self.button.grid(row=x, column=y)  
        self.button.bind('<Button-1>', self.showcell)
        self.button.bind('<Button-3>', self.placeflag)

    """Afficher ce qui se cache sous ce bouton par rapport à la grille donné lors de sa création lors qu'on fait un clic gauche 
    (afficher la value de chaque cellule)"""
    def showcell(self,e):
        widgets = self.frame.grid_slaves()
        nw = [widgets[i:i+self.grille.longueur] for i in range(0, len(widgets), self.grille.largeur)]
        if self.value=="X":
            tk.messagebox.showinfo(message="You lose")
            for widget in widgets:
                widget.unbind('<Button-1>')
                widget.unbind('<Button-3>')
                widget.config(state = DISABLED)
                if widget["text"]=="X":
                    widget.config( bg="red",fg="black")
                elif not widget["text"]=="X" and widget["bg"]=="grey":
                    widget.config(text="")
        if self.value=="0":
            self.grille.decouvrir(bouton =nw[self.grille.largeur-self.x-1][self.grille.largeur-self.y-1],x= self.x, y= self.y)
        if not self.value=="0" and not self.value=="X":
            self.button.config(bg="white",state=DISABLED,text=self.value)
        subset = [i for i in widgets if i["bg"]=="green"]
        self.grille.bombemax=self.grille.bombe - len(subset)
        self.labelbombe.config( text=f"Nombre de bombes à trouver : {self.grille.bombemax}")
        self.grille.checkwin()

    """Lors d'un clic droit, cette fonction colore le bouton en vert pour informer qu'on pense qu'il y a une bombe sous ce bouton"""
    def placeflag(self,e):
        widgets = self.frame.grid_slaves()
        subset = [i for i in widgets if i["bg"]=="green"]
        if self.grille.bombemax>0 and self.button["bg"]=="grey":
            self.grille.bombemax=self.grille.bombemax-1
            self.labelbombe.config( text=f"Nombre de bombes à trouver : {self.grille.bombemax}")
            self.button.config(bg="green", fg="green")
            self.grille.checkwin()
                
        elif self.button["bg"]=="green":
            self.grille.bombemax=self.grille.bombemax+1
            self.labelbombe.config( text=f"Nombre de bombes à trouver : {self.grille.bombemax}")
            self.button.config(bg="grey", fg="grey")
            self.grille.checkwin()
        
dem=Game()
dem.play()
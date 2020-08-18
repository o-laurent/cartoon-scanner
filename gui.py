"""from tkinter import *

# On crée une fenêtre, racine de notre interface
fenetre = Tk()

# On crée un label (ligne de texte) souhaitant la bienvenue
# Note : le premier paramètre passé au constructeur de Label est notre
# interface racine
champ_label = Label(fenetre, text="Entre le nom de l'image :")

# On affiche le label dans la fenêtre
champ_label.pack()

# Ligne de saisie
imgNameInput = StringVar()
ligne_texte = Entry(fenetre, textvariable=imgNameInput, width=30)
ligne_texte.pack()

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
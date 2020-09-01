# entrée valide 
# proposer un nom logique 
# afficher l'erreur 

from tkinter import Tk, Label, StringVar, Entry, Button

def graphical_user_interface():
    # On crée une fenêtre, racine de notre interface
    wdw = Tk()

    wdw.title('cartoon_scanner') # Ajout d'un titre

    label_field = Label(wdw, text="Entrer le nom de la série d'images :")
    label_field.pack()

    # Ligne de saisie
    img_name_input = StringVar()
    input_line = Entry(wdw, textvariable=img_name_input, width=30)
    input_line.pack()

    ok_btn = Button(wdw, text="OK", command=wdw.quit)
    ok_btn.pack()

    # On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
    wdw.mainloop()
    
    return img_name_input.get()
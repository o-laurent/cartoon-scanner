# entrée valide
# proposer un nom logique
# afficher l'erreur

from tkinter import Tk, Label, StringVar, Entry, Button, PhotoImage
from tkinter.ttk import Combobox

def graphical_user_interface(possibilities):
    """
    Graphical user interface for the cartoon scanner.
    It allows the user to choose the wanted parameters.

    Input:
    -possibility: List(str) default names of cartoon series 

    Output:
    -img_name_input: (str) name of the chosen cartoon series
    """
    # Create the window
    wdw = Tk()

    # Defining the title and the icon
    wdw.title('cartoon_scanner')
    wdw.iconphoto(False, PhotoImage(file='./src/icon/icon.png'))
    
    # Defining the fields
    label_field = Label(wdw, text="Choisissez le nom de la série d'images :")
    label_field.pack()

    input_line = Combobox(wdw, values=possibilities, width=30)
    input_line.set(possibilities[0])
    input_line.pack()

    ok_btn = Button(wdw, text="OK", command=wdw.quit)
    ok_btn.pack()

    # Starting window
    wdw.mainloop()
    wdw.quit()
    return input_line.get()

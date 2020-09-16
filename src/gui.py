# entrée valide
# proposer un nom logique
# afficher l'erreur

from tkinter import Tk, Label, Entry, Button, PhotoImage, Checkbutton
from tkinter import StringVar, IntVar
from tkinter.ttk import Combobox


def graphical_user_interface(possibilities):
    """
    Graphical user interface for the cartoon scanner.
    It allows the user to choose the wanted parameters.

    Input:
    - possibility: List(str) default names of cartoon series 

    Output:
    - img_name_input: (str) name of the chosen cartoon series
    - apple_correction: (int) compensate apple rotation flag
    - rotation_var: (int) true if rotation wanted
    - perspective_var: (int) true if perspective correction wanted
    - verbose_var: (int) true if verbose wanted
    - intermediate_var: (int) true if intermediate picture save wanted
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

    # Apple rotation flag correction
    apple_correction = IntVar(value=1)
    Checkbutton(wdw, text="Rotation Apple", variable=apple_correction).pack()

    # Perspective issue correction
    perspective_var = IntVar(value=1)
    Checkbutton(wdw, text="Correction de perspective",
                variable=perspective_var).pack()

    # Get more information
    verbose_var = IntVar()
    Checkbutton(wdw, text="Verbose", variable=verbose_var).pack()

    # Save intermidiate pictures
    intermediate_var = IntVar()
    Checkbutton(wdw, text="photo intermédiaires",
                variable=intermediate_var).pack()

    ok_btn = Button(wdw, text="OK", command=wdw.quit)
    ok_btn.pack()

    # Starting window
    wdw.mainloop()
    wdw.quit()
    return input_line.get(), apple_correction.get(), perspective_var.get(), verbose_var.get(), intermediate_var.get()

# This Python file is the main file that enables to run the contact book application.

from tkinter import Tk

from contact_book.src.contact_book.gui.application_window import \
    ApplicationWindow


class RunAPP:
    """
    The main class to run the contact book application, which opens a GUI for the user to perform
    CRUD operations (creating, reading, updating, deleting contacts), as well as clear the window.
    """
    tkinter_main_window = Tk()
    ApplicationWindow(tkinter_main_window)
    tkinter_main_window.mainloop()


if __name__ == "__main__":
    RunAPP()

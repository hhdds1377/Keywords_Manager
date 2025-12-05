import tkinter as tk

class MenuFile:
    def __init__(self,parent,menubar,*args,**kwargs):
        menu_edit=tk.Menu(menubar,tearoff=False)
        self.menu_edit=menu_edit

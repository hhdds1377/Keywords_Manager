import tkinter as tk
import sys,os
current_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(current_dir)
sys.path.append(parent_dir)
from .toplevel_add import ToplevelAdd

class MenuEdit:
    def __init__(self,parent,menubar,frame_find,scrt_pwd,db_path,*args,**kwargs):
        menu_edit=tk.Menu(menubar,tearoff=False)
        self.menu_edit=menu_edit

        def add_act(event):
            # 启动 toplevel_add
            ToplevelAdd(parent,scrt_pwd,db_path)
            
        def find_act(event):
            frame_find.grid(column=0,row=0,sticky='w')
            frame_find.entry_find.focus_set()

        def find_esc(event):
            frame_find.grid_remove()
        
        # 添加账号
        menu_edit.add_command(label='添加账号(A)',underline=5,accelerator='Ctrl+A',command=lambda :add_act(None))
        # 搜索账号
        menu_edit.add_command(label='搜索账号(F)',underline=5,accelerator='Ctrl+F',command=lambda :find_act(None))

        parent.bind('<Control-a>',add_act)
        parent.bind('<Control-f>',find_act)
        parent.bind('<Escape>',find_esc)

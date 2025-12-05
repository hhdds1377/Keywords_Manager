import tkinter as tk
from lib.pages.frame_accounts import FrameAccounts
from lib.pages.frame_accounts import FrameFind
from lib.pages.frame_info import FrameInfo
from lib.pages.menu_edit import MenuEdit
from lib.pages.menu_file import MenuFile
from lib.pages.menu_tools import MenuTools
from lib.pages.toplevel_start import ToplevelStart

class App(tk.Tk):
    def __init__(self,*args,**kwargs):
        # === 继承tk.Tk ===
        super().__init__(*args,**kwargs)

        # === 设置root的参数 ===
        self.title("Keywords Manager")
        w,h=600,400
        screen_w=self.winfo_screenwidth()
        screen_h=self.winfo_screenheight()
        x=(screen_w-w)//2
        y=(screen_h-h)//2
        self.geometry("{}x{}+{}+{}".format(w,h,x,y))
        self.columnconfigure(0,weight=0)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=0)
        self.rowconfigure(1,weight=1)
        self.withdraw()

        # === 启动toplevel_start ===
        toplevel_start=ToplevelStart(self,'./db/settings.json','./db/current.json')
        # 等待 toplevel_start 关闭
        self.wait_window(toplevel_start)
        scrt_pwd=toplevel_start.scrt_pwd

        # === 布局根窗口的控件 ===
        frame_accounts=FrameAccounts(self,'./db/current.json',scrt_pwd,padding=5)
        frame_find=FrameFind(self,frame_accounts.treeview,padding=5)
        frame_info=FrameInfo(self,frame_accounts,'./db/current.json','./img/copy.png',scrt_pwd,padding=5)
        frame_accounts.grid(column=0,row=1,sticky='ns')
        frame_info.grid(column=1,row=1,sticky='nsew')

        # === 布局根窗口的菜单 ===
        menubar=tk.Menu(self)
        self['menu']=menubar
        # 布局文件菜单
        MenuFile(self,menubar)
        # 布局编辑菜单
        menu_edit=MenuEdit(self,menubar,frame_find,scrt_pwd,'./db/current.json')
        menubar.add_cascade(label='编辑(E)',underline=3,menu=menu_edit.menu_edit)
        # 布局工具菜单
        MenuTools(self,menubar)

if __name__ == "__main__":
    with open('./temp_current.txt','rt',encoding='utf-8') as file:
        temp_current=file.read()
    with open('./db/current.json','wt',encoding='utf-8') as file:
        file.write(temp_current)
    with open('./temp_settings.txt','rt',encoding='utf-8') as file:
        temp_settings=file.read()
    with open('./db/settings.json','wt',encoding='utf-8') as file:
        file.write(temp_settings)
    app = App()
    app.mainloop()

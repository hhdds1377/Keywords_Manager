import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox
import os,sys
current_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(current_dir)
sys.path.append(parent_dir)
from decrypt import Decrypt
from encrypt import Encrypt

class ToplevelStart(tk.Toplevel):
    def __init__(self,parent,settings_path,db_path,*args,**kwargs):
        # 继承 tk.Toplevel 的 __init__ 方法
        super().__init__(parent,*args,**kwargs)

        # 使居中
        self.withdraw()
        self.update_idletasks()
        w=self.winfo_width()
        h=self.winfo_height()
        sw=self.winfo_screenwidth()
        sh=self.winfo_screenheight()
        x=(sw-w)//2
        y=(sh-h)//2
        self.geometry('+{}+{}'.format(x,y))
        self.deiconify()

        # 初始化数据
        self.scrt_pwd=None
        
        # 获得settings.json内容,如果没有获取到flag,初始化flag
        with open(settings_path,'rt',encoding='utf-8') as file:
            settings_dict=json.load(file)
        if settings_dict:
            if not settings_dict.get('pwd_generate_flag',False):
                settings_dict['pwd_generate_flag']=False
                with open(settings_path,'wt',encoding='utf-8') as file:
                    json.dump(settings_dict,file,indent=4)
        else:
            settings_dict={'pwd_generate_flag':False}
            with open(settings_path,'wt',encoding='utf-8') as file:
                json.dump(settings_dict,file,indent=4)
            

        # === 创建控件 ===
        # 创建密码输入控件
        frame_pwd_input=ttk.Frame(self,padding=5)
        frame_pwd_input.columnconfigure(0,weight=1)
        frame_pwd_input.rowconfigure(0,weight=1)
        frame_pwd_generate=ttk.Frame(self,padding=5)
        frame_pwd_generate.columnconfigure(0,weight=1)
        frame_pwd_generate.rowconfigure(0,weight=1)

        label_pwd=ttk.Label(frame_pwd_input,text='安全密码')
        entry_pwd=ttk.Entry(frame_pwd_input,show='*')

        label_pwd.grid(column=0,row=0,padx=(0,5))
        entry_pwd.grid(column=1,row=0)

        # 创建密码产生控件
        show_plain_var=tk.IntVar(master=self,value=0)
        label_ge_pwd=ttk.Label(frame_pwd_generate,text='设置安全密码')
        label_re_pwd=ttk.Label(frame_pwd_generate,text='重复安全密码')
        entry_ge_pwd=ttk.Entry(frame_pwd_generate,show='*')
        entry_re_pwd=ttk.Entry(frame_pwd_generate,show='*')
        def show_plain():
            if show_plain_var.get()==0:
                entry_ge_pwd['show']='*'
                entry_re_pwd['show']='*'
            elif show_plain_var.get()==1:
                entry_ge_pwd['show']=''
                entry_re_pwd['show']=''
        checkbtn_show_plain=ttk.Checkbutton(frame_pwd_generate,text='显示原文(S)',underline=5,onvalue=1,offvalue=0,variable=show_plain_var,command=show_plain)
        def invoke_checkbtn(event):
            checkbtn_show_plain.invoke()
        self.bind('<Alt-s>',invoke_checkbtn)

        label_ge_pwd.grid(column=0,row=0,padx=(0,5))
        label_re_pwd.grid(column=0,row=1,padx=(0,5))
        entry_ge_pwd.grid(column=1,row=0)
        entry_re_pwd.grid(column=1,row=1)
        checkbtn_show_plain.grid(column=0,row=2)

        # === 给控件绑定事件 ===
        # 密码输入
        if settings_dict['pwd_generate_flag']==True:
            frame_pwd_input.grid(column=0,row=0)
            entry_pwd.focus_set()
            def enter_root(event):
                # 尝试解密
                decrypt_obj=Decrypt(entry_pwd.get(),from_db_path=db_path)
                decrypt_obj.decrypt_file()
                if decrypt_obj.decrypt_success_flag==True:
                    self.scrt_pwd=entry_pwd.get()
                    self.destroy()
                    parent.deiconify()
                else:
                    messagebox.showinfo('错误提示','密码错误')
            entry_pwd.bind('<Return>',enter_root)
        # 密码创建
        else:
            frame_pwd_generate.grid(column=0,row=0)
            entry_ge_pwd.focus_set()
            def enter_next(event):
                entry_re_pwd.focus_set()
            def enter_root_generate(event):
                if entry_ge_pwd.get()==entry_re_pwd.get():
                    # 加密
                    if messagebox.askokcancel('确认是否加密','确认是否加密? 密码为:{}'.format(entry_ge_pwd.get()),default=['cancel']):
                        encrypt_obj=Encrypt(entry_ge_pwd.get(),from_db_path=db_path,to_db_path=db_path)
                        encrypt_obj.encrypt_file()
                        settings_dict['pwd_generate_flag']=True
                        with open(settings_path,'wt',encoding='utf-8') as file:
                            json.dump(settings_dict,file,indent=4)
                        self.scrt_pwd=entry_ge_pwd.get()
                        self.destroy()
                        parent.deiconify()
                else:
                    messagebox.showinfo('错误提示','两次输入的密码不相同')
            entry_ge_pwd.bind('<Return>',enter_next)
            entry_re_pwd.bind('<Return>',enter_root_generate)

if __name__=='__main__':
    # 测试
    root=tk.Tk()
    root.withdraw()
    top=ToplevelStart(root,'../../db/settings.json','../../db/current.json')
    root.mainloop()

import tkinter as tk
from tkinter import ttk
import sys,os
current_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(current_dir)
sys.path.append(parent_dir)
from decrypt import Decrypt
from encrypt import Encrypt
from tkinter import messagebox
import time
from frame_accounts import FrameAccounts

class ValidateSpinbox(ttk.Spinbox):
    def __init__(self,parent,from_,to,*args,**kwargs):
        if 'textvariable' in kwargs:
            self.var=kwargs['textvariable']
        else:
            self.var=tk.StringVar()
            kwargs['textvariable']=self.var

        super().__init__(parent,from_=from_,to=to,validate='key',*args,**kwargs)

        self.from_=from_
        self.to=to

        self.last_valid_value=str(from_)

        vcmd=(self.register(self._validate),'%P')
        self.config(validatecommand=vcmd)

        self.var.set(self.last_valid_value)

        self.bind('<FocusOut>',self._on_focus_out)

        if 'command' in kwargs:
            self._user_command = kwargs['command']
            self.var.trace_add('write', lambda *args: self._user_command())

    def _validate(self,proposed):
        if proposed=='':
            return True
        
        if not proposed.isdigit():
            return False
        
        value=int(proposed)

        if self.from_<=value<=self.to:
            self.last_valid_value=proposed
            return True
        
        self.var.set(self.last_valid_value)
        return False
    
    def _on_focus_out(self,event):
        if self.var.get()=='' or not self.var.get().isdigit():
            self.var.set(self.last_valid_value)
        else:
            value=int(self.var.get())
            if value<self.from_ or value>self.to:
                self.var.set(self.last_valid_value)

class ToplevelAdd(tk.Toplevel):
    def __init__(self,parent,scrt_pwd,db_path,*args,**kwargs):
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

        # === 创建控件 ===
        # 创建条目输入控件
        frame_db_input=ttk.Frame(self,padding=5)
        frame_db_input.grid(column=0,row=0,sticky='nsew')

        # 创建设置条目
        label_necessary_item=ttk.Label(frame_db_input,text='设置条目',anchor='w')
        label_front=ttk.Label(frame_db_input,text='键',anchor='w')
        label_back=ttk.Label(frame_db_input,text='值',anchor='w')

        label_necessary_item.grid(column=0,row=0,columnspan=2,sticky='ew')
        label_front.grid(column=0,row=1,sticky='ew')
        label_back.grid(column=1,row=1,sticky='ew')

        label_account=ttk.Label(frame_db_input,text='账号',anchor='w')
        label_notes=ttk.Label(frame_db_input,text='说明',anchor='w')
        label_layer=ttk.Label(frame_db_input,text='层次',anchor='w')

        label_account.grid(column=0,row=2,sticky='ew')
        label_notes.grid(column=0,row=3,sticky='ew')
        label_layer.grid(column=0,row=4,sticky='ew')

        account_var=tk.StringVar(self,None)
        entry_account=ttk.Entry(frame_db_input,textvariable=account_var)
        notes_var=tk.StringVar(self,None)
        notes_account=ttk.Entry(frame_db_input,textvariable=notes_var)

        label_parent_account=ttk.Label(frame_db_input,text='账号夹',anchor='w')
        layer_var=tk.StringVar(self,'0')
        parent_var=tk.StringVar(self,None)
        entry_parent=ttk.Entry(frame_db_input,textvariable=parent_var)
        def show_parent(*args):
            val=layer_var.get()
            if val=='':
                val='0'
            if int(val)==1:
                label_parent_account.grid(column=0,row=5)
                entry_parent.grid(column=1,row=5,sticky='ew')
            else:
                label_parent_account.grid_remove()
                entry_parent.grid_remove()
        
        def check_parent():
            parent_list=[]
            decrypt_obj=Decrypt(scrt_pwd,from_db_path=db_path)
            decrypt_obj.decrypt_file()
            db_list=decrypt_obj.plaintext
            for db_child in db_list:
                if db_child['layer']==0:
                    parent_list.append(db_child['account'])
            if not parent_var.get() in parent_list:
                messagebox.showerror('匹配错误','未在已创建的账号夹中匹配到任何账号夹')
                self.entry_parent.focus_set()
                return False
            else:
                return True

        spinbox_layer=ValidateSpinbox(frame_db_input,from_=0,to=1,textvariable=layer_var,command=show_parent,wrap=True)

        entry_account.grid(column=1,row=2,sticky='ew')
        notes_account.grid(column=1,row=3,sticky='ew')
        spinbox_layer.grid(column=1,row=4,sticky='ew')

        # 创建信息条目
        label_unnecessary_item=ttk.Label(frame_db_input,text='信息条目',anchor='w')
        label_itemnum=ttk.Label(frame_db_input,text='条目数量',anchor='w')
        itemnum_var=tk.StringVar(self,'2')
        self.info_entries=[]
        def add_item(*args):
            val=itemnum_var.get()
            if val=='' or not val.isdigit():
                val='2'
            
            current_values=[[key.get(),value.get()] for key,value in self.info_entries]

            while len(self.info_entries)>int(val):
                key,value=self.info_entries.pop()
                key.destroy()
                value.destroy()
            while len(self.info_entries)<int(val):
                entry_key=ttk.Entry(frame_db_input)
                entry_value=ttk.Entry(frame_db_input)
                self.info_entries.append((entry_key,entry_value))
            
            for i,(key,value) in enumerate(self.info_entries):
                key.grid(column=2,row=3+i,sticky='ew')
                value.grid(column=3,row=3+i,sticky='ew')
                if i<len(current_values):
                    key.delete(0,tk.END)
                    key.insert(0,current_values[i][0])
                    value.delete(0,tk.END)
                    value.insert(0,current_values[i][1])
        spinbox_itemnum=ValidateSpinbox(frame_db_input,from_=2,to=8,textvariable=itemnum_var,wrap=True,command=add_item)
        label_key=ttk.Label(frame_db_input,text='键',anchor='w')
        label_value=ttk.Label(frame_db_input,text='值',anchor='w')

        label_unnecessary_item.grid(column=2,row=0,columnspan=2,sticky='ew')
        label_itemnum.grid(column=2,row=1,sticky='ew')
        spinbox_itemnum.grid(column=3,row=1,sticky='ew')
        label_key.grid(column=2,row=2,sticky='ew')
        label_value.grid(column=3,row=2,sticky='ew')
        def generate_item(*args):
            for add_num in range(int(itemnum_var.get())):
                entry_key=ttk.Entry(frame_db_input)
                entry_value=ttk.Entry(frame_db_input)

                entry_key.grid(column=2,row=3+add_num,sticky='ew')
                entry_value.grid(column=3,row=3+add_num,sticky='ew')
                self.info_entries.append((entry_key,entry_value))
        generate_item()

        # 创建保存按钮
        def save():
            # 整理数据
            child_dict={}
            child_dict['account']=account_var.get().strip()
            child_dict['notes']=notes_var.get().strip()
            child_dict['layer']=layer_var.get()
            child_dict['parent_account']=parent_var.get().strip()
            child_dict['info']=[[key.get(),value.get()] for key,value in self.info_entries if key.get().strip() and value.get().strip()]
            child_dict['create_time']=time.strftime('%m/%d/%Y',time.localtime(time.time()))
            child_dict['edit_time']=time.strftime('%m/%d/%Y',time.localtime(time.time()))
            if account_var.get():
                if int(layer_var.get())==1:
                    if check_parent():
                        decrypt_obj=Decrypt(scrt_pwd,from_db_path=db_path)
                        decrypt_obj.decrypt_file()
                        plaintext=decrypt_obj.plaintext
                        plaintext.append(child_dict)
                        encrypt_obj=Encrypt(scrt_pwd,data=plaintext,to_db_path=db_path)
                        encrypt_obj.encrypt_data()
                    else:
                        return
                else:
                    decrypt_obj=Decrypt(scrt_pwd,from_db_path=db_path)
                    decrypt_obj.decrypt_file()
                    plaintext=decrypt_obj.plaintext
                    plaintext.append(child_dict)
                    encrypt_obj=Encrypt(scrt_pwd,data=plaintext,to_db_path=db_path)
                    encrypt_obj.encrypt_data()
                
                self.destroy()
        btn_save=ttk.Button(frame_db_input,text='保存',command=save)
        btn_save.grid(column=5,row=1)

        btn_cancel=ttk.Button(frame_db_input,text='取消',command=self.destroy)
        btn_cancel.grid(column=5,row=2)

if __name__=='__main__':
    root=tk.Tk()
    root.withdraw()
    toplevel_add=ToplevelAdd(root,'123','../../db/current.json')
    root.mainloop()
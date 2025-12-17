import tkinter as tk
from tkinter import ttk
import sys,os
current_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(current_dir)
sys.path.append(parent_dir)
from decrypt import Decrypt
from encrypt import Encrypt

class TreeviewAccounts(ttk.Treeview):
    def __init__(self,parent,db_path,scrt_pwd,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)

        self.config(columns=('notes',),padding=3,show='tree headings')
        self.column('#0',width=140,stretch=False)
        self.column('#1',width=140,stretch=False)
        self.heading('#0',text='账号',anchor='w')
        self.heading('#1',text='说明',anchor='w')

        decrypt_obj=Decrypt(scrt_pwd,from_db_path=db_path)
        decrypt_obj.decrypt_file()
        db_list=decrypt_obj.plaintext

        db_list.sort(key=lambda i:int(i['layer']))
        accounts_iid_dict={}
        for item_index,item_dict in enumerate(db_list):
            if item_dict['layer']==0:
                iid_layer0=self.insert('','end',text=item_dict['account'],values=(item_dict['notes'],))
                item_dict['iid']=iid_layer0
                db_list[item_index]=item_dict
                accounts_iid_dict[item_dict['account']]=item_dict['iid']
            elif item_dict['layer']==1:
                iid_layer1=self.insert(accounts_iid_dict[item_dict['parent_account']],'end',text=item_dict['account'],values=(item_dict['notes'],))
                item_dict['iid']=iid_layer1
                db_list[item_index]=item_dict

        encrypt_obj=Encrypt(scrt_pwd,data=db_list,to_db_path=db_path)
        encrypt_obj.encrypt_data()

class FrameAccounts(ttk.Frame):
    def __init__(self,parent,db_path,scrt_pwd,*args,**kwargs):
        super().__init__(parent)

        self.config(width=300,height=600)
        self.grid_propagate(False)

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1,weight=0,minsize=15)

        treeview=TreeviewAccounts(self,db_path,scrt_pwd)
        self.treeview=treeview
        treeview.grid(column=0,row=0,sticky='nsew')

        yscrollbar=ttk.Scrollbar(self)
        yscrollbar.grid(column=1,row=0,sticky='ns')
        yscrollbar.config(command=treeview.yview)
        treeview.configure(yscrollcommand=yscrollbar.set)

        xscrollbar=ttk.Scrollbar(self,orient='horizontal')
        xscrollbar.grid(column=0,row=1,sticky='ew')
        xscrollbar.config(command=treeview.xview)
        treeview.configure(xscrollcommand=xscrollbar.set)


class FrameFind(ttk.Frame):
    def __init__(self,parent,treeview,*args,**kwargs):
        super().__init__(parent)
        self.config(padding=3,width=250)

        var_find=tk.StringVar(self)
        entry_find=ttk.Entry(self,textvariable=var_find,width=30)
        self.entry_find=entry_find
        treeview.tag_configure('highlight',background='#FFD700')
        
        l0_found_iid_list=[]
        l1_found_iid_list=[]
        def item_highlight(event):
            if not var_find.get().strip():
                return
            found_flag=0 
            nonlocal l0_found_iid_list
            nonlocal l1_found_iid_list
            if l0_found_iid_list:
                treeview.item(l0_found_iid_list[-1],tags=('',))
            if l1_found_iid_list:
                treeview.item(l1_found_iid_list[-1],tags=('',))
            for l0_item_iid in treeview.get_children():
                if l0_item_iid not in l0_found_iid_list:
                    if var_find.get().strip() in treeview.item(l0_item_iid,'text'):
                        treeview.see(l0_item_iid)
                        treeview.item(l0_item_iid,tags=('highlight',))
                        l0_found_iid_list.append(l0_item_iid)
                        found_flag+=1
                        return

                if treeview.get_children(l0_item_iid):
                    for l1_item_iid in treeview.get_children(l0_item_iid):
                        if l1_item_iid not in l1_found_iid_list:
                            if var_find.get().strip() in treeview.item(l1_item_iid,'text'):
                                treeview.item(l0_item_iid,open=True)
                                treeview.see(l1_item_iid)
                                treeview.item(l1_item_iid,tags=('highlight',))
                                l1_found_iid_list.append(l1_item_iid)
                                found_flag+=1
                                return

            if found_flag==0:
                if l0_found_iid_list or l1_found_iid_list:
                    l0_found_iid_list=[]
                    l1_found_iid_list=[]
                    return item_highlight(event)
                else:
                    return
                
        entry_find.bind('<Return>',item_highlight)
        entry_find.grid(column=1,row=0,sticky='ew')

        label_find=ttk.Label(self,text='>')
        label_find.grid(column=0,row=0)

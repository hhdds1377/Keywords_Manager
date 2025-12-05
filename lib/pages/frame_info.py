import tkinter as tk
from tkinter import ttk
import pyperclip
from PIL import Image,ImageTk
import os,sys
current_dir=os.path.dirname(os.path.abspath(__file__))
parent_dir=os.path.dirname(current_dir)
sys.path.append(parent_dir)
from decrypt import Decrypt

class FrameInfo(ttk.Frame):
    def __init__(self,parent,frame_accounts,db_path,img_path,scrt_pwd,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)

        img=Image.open(img_path)
        img=img.resize((18,18),Image.Resampling.LANCZOS)
        self.img=ImageTk.PhotoImage(img)
        # === Canvas 用来滚动 ===
        self.canvas=tk.Canvas(self,highlightthickness=0)
        self.canvas.grid(column=0,row=0,sticky='nsew')

        self.v_scroll=ttk.Scrollbar(self,orient='vertical',command=self.canvas.yview)
        self.v_scroll.grid(row=0,column=1,sticky='ns')

        self.h_scroll=ttk.Scrollbar(self,orient='horizontal',command=self.canvas.xview)
        self.h_scroll.grid(row=1,column=0,sticky='ew')


        # === 内部 Frame ===
        self.inner=ttk.Frame(self.canvas)
        self.inner_id=self.canvas.create_window((0,0),window=self.inner,anchor='nw')

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1, weight=0)

        self.canvas.columnconfigure(0,weight=1)
        self.canvas.rowconfigure(0,weight=1)

        self.inner.columnconfigure(0,weight=1)
        self.inner.columnconfigure(1,weight=1)
        self.inner.columnconfigure(2,weight=1)

        # === 绑定事件:更新滚动区域 ===
        self.inner.bind('<Configure>',self._on_frame_config)
        self.canvas.bind('<Configure>',self._on_canvas_config)

        # === 绑定鼠标滚动 ===
        self._bind_mousewheel()

        # === frame_accounts 绑定点击 ===
        self.before_widget_list=[]
        def show_info(event):
            if self.before_widget_list:
                for widget_obj in self.before_widget_list:
                    widget_obj.grid_remove()
            self.before_widget_list.clear()
            # 引用 treeview
            treeview=event.widget

            # 引用点击的 item 的 iid
            if not treeview.selection():
                return
            item_select_iid=treeview.selection()[0]

            # 通过 iid 定位数据
            decrypt_obj=Decrypt(scrt_pwd,from_db_path=db_path)
            decrypt_obj.decrypt_file()
            db_list=decrypt_obj.plaintext
            for item in db_list:
                item_dict_iid=item['iid']
                if item_dict_iid==item_select_iid:
                    item_dict=item
                    break
            else:
                return

            if item_dict['layer']==0:
                head_label=ttk.Label(self.inner,text='{}\n创建时间: {}\t编辑时间: {}'.format(item_dict['account'],item_dict['create_time'],item_dict['edit_time']),anchor='w')
            else:
                head_label=ttk.Label(self.inner,text='{} >> {}\n创建时间: {}\t编辑时间: {}'.format(item_dict['parent_account'],item_dict['account'],item_dict['create_time'],item_dict['edit_time']),anchor='w')
            
            head_label.grid(column=0,row=0,columnspan=3,sticky='ew')
            self.before_widget_list.append(head_label)

            info_list=item_dict['info']
            if info_list:
                for info_index,info_tuple in enumerate(info_list):
                    front_label=ttk.Label(self.inner,text=info_tuple[0],anchor='w',width=10)
                    back_label=ttk.Label(self.inner,text=info_tuple[1],anchor='w',width=20)
                    def copy_info():
                        pyperclip.copy(back_label['text'])
                    copy_btn=ttk.Button(self.inner,image=self.img,command=copy_info)

                    front_label.grid(column=0,row=info_index+1,sticky='ew')
                    back_label.grid(column=1,row=info_index+1,sticky='ew')
                    copy_btn.grid(column=2,row=info_index+1)

                    self.before_widget_list.extend([front_label,back_label,copy_btn])
            else:
                return
            
        frame_accounts.treeview.bind('<ButtonRelease-1>',show_info)
        

    # === 当 inner Frame 大小变化时更新可滚动区域 ===
    def _on_frame_config(self, event):
        # 限制 scrollregion 下边界至少为 canvas 当前高度
        self.canvas.update_idletasks()
        canvas_height = self.canvas.winfo_height()
        bbox = list(self.canvas.bbox("all"))

        if bbox is None:
            return

        # 如果内容高度 < canvas 高度 → 强制 scrollregion 高度 = canvas 高度
        if bbox[3] < canvas_height:
            bbox[3] = canvas_height

        self.canvas.configure(scrollregion=tuple(bbox))

    # === 当 Canvas 大小变化时,自动调整 inner 的宽度(用于 ttk 样式兼容) ===
    def _on_canvas_config(self,event):
        canvas_width = event.width
        inner_req_width = self.inner.winfo_reqwidth()

        if inner_req_width < canvas_width:
            # 让它撑满
            self.canvas.itemconfig(self.inner_id, width=canvas_width)
        else:
            # 内容宽度超过 canvas，不要强行撑满
            self.canvas.itemconfig(self.inner_id, width=inner_req_width)

    # === 鼠标滚动绑定 ===
    def _bind_mousewheel(self):
        # Windows / Linux
        self.canvas.bind_all('<MouseWheel>',self._on_mousewheel)
        self.canvas.bind_all('<Shift-MouseWheel>',self._on_shift_mousewheel)

        # macOS  (滚动事件名不同)
        self.canvas.bind_all('<Button-4>',lambda e: self.canvas.yview_scroll(-1,'units'))
        self.canvas.bind_all('<Button-5>',lambda e: self.canvas.yview_scroll(1,'units'))

    def _on_mousewheel(self,event):
        self.canvas.yview_scroll(-1*(event.delta//120),'units')

    def _on_shift_mousewheel(self,event):
        # 按住 Shift 滚动 横向
        self.canvas.xview_scroll(-1*(event.delta//120),'units')

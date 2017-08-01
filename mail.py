from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import smtplib
import os
#import _md5
import  tkinter as tk
import shelve
from email.mime.text import MIMEText
from email.utils import formataddr
# from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from tkinter import ttk
from tkinter import simpledialog


class User:
    def  __init__(self):
        try:
            # print(os.path.split(os.path.realpath(__file__)))
            os.chdir(os.path.split(os.path.realpath(__file__))[0])
            self.db = shelve.open('user.db', flag='c', writeback=True)

        except:
            tkinter.messagebox.showinfo('打开失败')
            frame.close(event='')
    def creat(self,account,password,address):
        if not 'num'in self.db:
            self.db['num'] = 0
            self.db['user'] = {'user':[]}
        if account in self.db:
            tkinter.messagebox.showinfo("邮箱","已存在")
            return
        if len(account)==0 :
            tkinter.messagebox.showinfo("邮箱","账号不能为空")
            return
        self.db[account]={'password':password, 'address':address}
        self.db['num']+=1
        self.db['user']['user'].append(account)
        self.db.sync()

    def userget(self):
        try:
            userlist = self.db['user']['user']
            return userlist
        except:
            return []

    def userdel(self,num,account):
        if  len(account)!=0:
            del self.db[account]
            self.db['user']['user'].remove(account)
            self.db['num'] -= 1
            #self.db.close()
        else: raise Exception
    def userrefresh(self):
        self.db.close()
        userlist.__init__()
        return self.userget()
    def userinfoget(self,account):
        password = self.db[account]['password']
        address = self.db[account]['address']
        return password,address

class MainWindow:

    my_sender = ''  # 发件人邮箱账号
    my_password = ''  # 发件人邮箱密码
    my_receiver = ''  # 收件人邮箱账号
    my_address = ''  # 邮件服务器地址
    file_name = ''
    # 适配器
    def sendadaptor(self, fun, **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)
    def filechooseadaptor(self,fun,**kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event,**kwds)
    def closeadaptor(self,fun,**kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event,**kwds)
    def usercreatadaptor(self,fun,**kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event,**kwds)
    def userdeladaptor(self, fun, **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)
    def close(self,fun,**kwds):
        self.root.destroy()


    #发送邮件
    def send(self,event,filename):
        msg = MIMEMultipart('alternative')
        self.my_sender = self.myCombox.get()
        self.my_receiver =  self.text_receiver.get("0.0", "end")
        self.my_password, self.my_address = userlist.userinfoget(self.my_sender)
        #receiver = self.text_receiver.get("0.0", "end") if(self.text_receiver.get("0.0", "end")) else "未指定"
        subject = self.text_title.get("0.0", "end") if(self.text_title.get("0.0", "end")) else "未指定"
        index = MIMEText(self.text_index.get("0.0", "end"),'plain')
        att1 = MIMEBase('application', 'octet-stream')
        msg['From'] = formataddr(['', self.my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(['', self.my_receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = subject  # 邮件的主题，也可以说是标题
        msg.attach(index)

        if self.file_name:
            try:
                with open(self.file_name)as fp:
                    att1.set_payload(fp.read())
                    encoders.encode_base64(att1)
                    att1.add_header('Content-Disposition', 'attachment; filename="test.txt"')
                    msg.attach(att1)
            except Exception:
                tkinter.messagebox.showinfo("邮箱","附件添加失败")
        if self.my_receiver:
            server = smtplib.SMTP()
            server.connect(self.my_address)
            server.login(self.my_sender, self.my_password)
            server.sendmail(self.my_sender, [self.my_receiver, ], msg.as_string())
            server.quit()
            tkinter.messagebox.showinfo("邮箱","发送成功")
            self.text_receiver.delete(0.0,END)
            self.text_title.delete(0.0,END)
            self.text_index.delete(0.0,END)
            self.text_filechoose.delete(0.0,END)
        else:tkinter.messagebox.showinfo("邮箱","收件人不能为空")
    #读入文件
    def filechoose(self,event):
        self.file_name = tkinter.filedialog.askopenfilename(filetypes=[("文件", "*.*")])
        self.text_filechoose.delete(1.0,tkinter.END)
        self.text_filechoose.insert(1.0,self.file_name)
        # print(file_name)


    def usercreat(self,event):
        account = simpledialog.askstring('邮箱','请输入账号',initialvalue='example@xx.xxx')
        password = simpledialog.askstring('邮箱', '请输入密码', show='*')
        address = simpledialog.askstring('邮箱', '请输入地址')
        if not account:
                tkinter.messagebox.showinfo("邮箱","账号不能为空，创建失败")
                return
        elif not password:
                tkinter.messagebox.showinfo("邮箱","密码不能为空，创建失败")
                return
        elif not address:
                tkinter.messagebox.showinfo("邮箱","地址不能为空，创建失败")
                return
        try:
            userlist.creat(account=account, password=password, address=address)
            #self.myCombox = ttk.Combobox(self.root, width=20, state='readonly', value=myComboList)
            self.userlistrefresh()
            #self.__init__()
            tkinter.messagebox.showinfo("邮箱","创建成功！")

        except:tkinter.messagebox.showinfo("邮箱","创建失败")

        '''usercreatframe = Tk()
        usercreatframe.title("新增")
        usercreatframe.label_account = Label(usercreatframe, text="账号:")
        usercreatframe.label_account.grid(row=0, column=0)
        usercreatframe.label_password = Label(usercreatframe, text="密码:")
        usercreatframe.label_password.grid(row=1, column=0)
        usercreatframe.label_address = Label(usercreatframe, text="地址:")
        usercreatframe.label_address.grid(row=2, column=0)
        usercreatframe.text_account = Text(usercreatframe, height="1", width=30)
        usercreatframe.text_account.grid(row=0, column=1)
        usercreatframe.text_password_var = StringVar()
        usercreatframe.text_password = tkinter.Entry(usercreatframe, textvariable=usercreatframe.text_password_var, show='*')
        usercreatframe.text_password.grid(row=1, column=1)'''
    def userdel(self,event):
        try:
            num = self.myCombox.current() + 1
            account = self.myCombox.get()
            userlist.userdel(num=num, account=account)
            self.userlistrefresh()
            tkinter.messagebox.showinfo("邮箱","删除成功")

        except:
            tkinter.messagebox.showinfo("邮箱","删除失败")
    def userlistrefresh(self):
        mycombolist = list(userlist.userrefresh())
        #self.myCombox = ttk.Combobox(self.root, value=mycombolist)
        #self.myCombox.set(value=mycombolist)
        self.myCombox.configure(value=mycombolist)
        root.update_idletasks()
    #初始化布局
    def __init__(self,master=None):

        self.root = master
        self.label_user = Label(self.root, text="选择账号:")
        self.label_receiver = Label(self.root, text="   收件人:")
        self.label_title = Label(self.root, text="邮件标题:")
        self.label_index = Label(self.root, text="邮件内容:")
        self.label_file = Label(self.root, text="选择附件:")

        myComboList = userlist.userget()
        # name = StringVar()  textvariable=name, show='*'
        self.myCombox = ttk.Combobox(self.root, width=20, state='readonly', value=myComboList)
        #self.myCombox.bind("<<ComboboxSelected>>", self.userlistrefreshadaptor(self.userlistfresh))

        self.text_receiver = Text(self.root, height="1", width=30)
        self.text_title = Text(self.root, height="1", width=30)
        self.text_index = Text(self.root, height="3", width=30)
        self.text_filechoose = Text(self.root, height="2", width=30)

        # self.button_send = Button(self.root, text="发送", width=10,command=lambda :self.send(filename=file_name))
        self.button_send = Button(self.root, text="发送", width=10)
        self.button_close = Button(self.root, text="关闭", width=10)
        self.button_filechoose = tkinter.Button(self.root, text="选择文件", width=10, height=1)
        self.button_usercreat = Button(self.root, text="新增", width=10)
        self.button_userdel = Button(self.root, text="删除", width=10)

        # 通过中介函数进行事件绑定
        self.button_send.bind("<Button-1>", self.sendadaptor(self.send, filename=self.file_name))
        self.button_filechoose.bind("<Button-1>", self.filechooseadaptor(self.filechoose))
        self.button_close.bind("<Button-1>",self.closeadaptor(self.close))
        self.button_usercreat.bind("<Button-1>",self.usercreatadaptor(self.usercreat))
        self.button_userdel.bind("<Button-1>",self.userdeladaptor(self.userdel))

        self.myCombox.grid(row=0,column=1)
        self.label_user.grid(row=0, column=0)
        self.label_receiver.grid(row=1, column=0)
        self.label_title.grid(row=2, column=0)
        self.label_index.grid(row=3, column=0)
        self.label_file.grid(row=5, column=0)

        self.text_receiver.grid(row=1, column=1)
        self.text_title.grid(row=2, column=1)
        self.text_index.grid(row=3, column=1)
        self.text_filechoose.grid(row=5, column=1)

        self.button_send.grid(row=7, column=0)
        self.button_close.grid(row=7, column=1)
        self.button_filechoose.grid(row=5, column=2)
        self.button_usercreat.grid(row=0, column=2)
        self.button_userdel.grid(row=0, column=3)

if __name__=="__main__":
    userlist = User()
    root = tk.Tk()
    root.title("邮件")
    window_frame = MainWindow(root)
    root.mainloop()


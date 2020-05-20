import cv2 as cv
import numpy as np
import tkinter as tk
import tkinter.messagebox , threading
from PIL import ImageTk, Image
import cvui,time,os,webbrowser
import win32gui,win32api,win32con
class Page(object):
    def __init__(self,height = 400 , width = 500 , window = "Page" , background = None):
        self.WindowHeight = height
        self.WindowWidth = width
        self.WindowName = window
        self.BackGround = background
    def LoadBackground(self,src):
        img = Image.open(src)
        img = img.resize((self.WindowWidth,self.WindowHeight))
        photo = ImageTk.PhotoImage(img)
        self.BackGround = photo
    def BuildBackground(self,src):
        photo = self.LoadBackground(src)
        canvas = tk.Canvas(self.master,
                           width=self.WindowWidth,
                           height=self.WindowHeight)
        canvas.create_image(self.WindowWidth / 2,self.WindowHeight / 2,image=self.BackGround)
        canvas.pack()
    def CalCenter(self):
        ScreamWidth = self.master.winfo_screenwidth()
        ScreamHeight = self.master.winfo_screenheight()
        x = ScreamWidth / 2 - self.WindowWidth / 2
        y = ScreamHeight / 2 - self.WindowHeight / 2
        self.master.geometry('%dx%d+%d+%d' % (self.WindowWidth, self.WindowHeight, x, y))
        # print('cal:', x ,y , ScreamWidth , ScreamHeight)
        self.master.grid()
    def SetBox(self,x,y,width=250,height=30,name=None):
        box = tk.StringVar(name=None)
        BoxLink = tk.Entry(self.master,textvariable=box)
        BoxLink.place(x=x, y=y, width=width, height=height)
        return BoxLink
    def SetLabel(self,x,y,width=90,height=30,name = None):
        Label = tk.Label(self.master,text = name,font=("Arial", 14))
        Label.place(x=x,y=y,width=width,height=height)
    def SetButton(self,Fun,x=60,y=200,width=100,height=30,txt=None):
        Button = tk.Button(self.master, text=txt, command=Fun,font=("Arial", 14))
        Button.place(x=x, y=y, width=width, height=height)
    # def Print(self):
    #     print('--------------')
    #     print('start to initialize father element')
    #     print('--------------')
class LoginWindow(Page):
    def __init__(self,height = 400 , width = 500 , window = "LoginPage" , background = None):
        self.master = tk.Tk()
        super().__init__(height=height,width = 500,window = "LoginPage",background = background)
        self.Setting()
    # def Print(self):
    #     print(self.WindowHeight , self.WindowName , self.WindowWidth)
    #     print('successfully initialize')
    def Startup(self):
        self.master.title(self.WindowName)
        self.master['width'] = self.WindowWidth
        self.master['height'] = self.WindowHeight
        self.CalCenter()
        tk.mainloop()
    def Login(self):
        # if self.User.get() == 'admin' and self.password.get() == 'chm0402':
        #     self.master.destroy()
        #     MainPage()
        # else:
        #     msg = 'user or password is error , try again please '
        #     tk.messagebox.showinfo(title='error',message=msg)
        # pass
        self.master.destroy()
        MainPage()
    def Logout(self):
        self.master.destroy()
        pass
    def BuildMenu(self,MenuName):
        menu = tk.Menu(self.master)
        SubMenu = tk.Menu(menu,tearoff=False)
        SubMenu.add_command(label='about', command=self.About)
        SubMenu.add_command(label='info', command=self.information)
        menu.add_cascade(label=MenuName,menu=SubMenu)
        self.master.config(menu=menu)
    def Setting(self):
        src = 'rabbit.jpg'
        self.BuildBackground(src=src)
        user = self.SetBox(170,200,name = 'User')
        pd = self.SetBox(170,250,name = 'Password')
        self.User = user
        self.password = pd
        self.SetLabel(70,200,name = 'User')
        self.SetLabel(70,250,name = 'Password')
        self.SetButton(self.Login,x=120,y=300,txt='login')
        self.SetButton(self.Logout,x=270,y=300,txt='logout')
        self.BuildMenu('Help')
        self.Startup()
    def About(self):
        msg = '''
        Welcome to my world. this Application is designed by me .
        if u wanna use the app . correctly show the Information .
        thank u for
        '''
        tk.messagebox.showinfo(title='about',message=msg)
    def information(self):
        msg='''
        作者：CaoHaiMing
        邮箱：hoiming.wk@foxmail.com
        '''
        tkinter.messagebox.showinfo(title='Info', message=msg)
class MainPage(Page):
    def __init__(self,height = 800 , width = 1600 , window = "MainPage",background = None):
        self.master = tk.Tk()
        super().__init__(height = height , width = width , window = window,background = background)
        self.Setting()
    def Setting(self):
        self.master.title(self.WindowName)
        src = 'wallpaper.jpg'
        self.BuildBackground(src=src)
        self.CalCenter()
        self.SetButton(self.Back,x=200,y=500,width=190,txt="Back to Login Page")
        self.SetButton(self.Capture,x=400,y=500,width=190,txt='Capture')
        # os.system('pause')
    def Back(self):
        self.master.destroy()
        LoginWindow()
    def Capture(self):
        # self.master.destroy()
        CapturePage()
        # MainPage()
class CapturePage(object):
    def __init__(self,width=600,height=1000,name='window',BGcolor=(49, 52, 49)):
        self.WindowWidth = width
        self.WindowHeight = height
        self.color = BGcolor
        self.WindowName = name
        self.capture = cv.VideoCapture(0)
        self.Setting()
    def Setting(self):
        wallpaper = cv.imread('wallpaper.jpg')
        frame = cv.resize(wallpaper , (self.WindowHeight,self.WindowWidth))
        x = 1920 / 2 - self.WindowWidth / 2
        y = 1080 / 2 - self.WindowHeight / 2
        # print(x, y)
        # cv.namedWindow(winname=self.WindowName)
        cvui.init(self.WindowName)
        cv.moveWindow(winname=self.WindowName,x=450,y=190)
        cur = frame
        choose = 0
        signin = '2020-05-20 08:00:00'
        text = ''
        set = 0
        while True:
            # frame[:] = self.color
            frame = cv.resize(wallpaper , (self.WindowHeight,self.WindowWidth))
            status , cap = self.capture.read()
            cap = cv.resize(cap,(500,500))
            cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            cvui.printf(frame , 30 ,50, 0.7,0xff0000,"current time : %s"  , cur_time)
            cvui.printf(frame , 30 ,70, 0.7,0xff0000,"signin  time : %s"  , signin)
            if cvui.button(frame, 30, 110, 'Linux Button') == True:
                choose = 1
                signin = '2020-05-20 08:00:00'
                # signin = '2020-05-20 01:46:30' #test

            if cvui.button(frame, 150, 110, 'Program Button') == True:
                choose = 0
                signin = '2020-05-21 07:58:00'
            if cvui.button(frame ,300  , 110 , 'set name') == True:
                set = set ^ 1
            cvui.image(frame , 490,10,cap)
            cvui.printf(frame , 30 ,200, 0.7,0xff0000,"your choice : %s"  , 'Linux' if choose == 1 else 'Program')
            if set == 1:
                cv.putText(frame , 'your name :' + text , (30,300) , cv.FONT_HERSHEY_COMPLEX, 1.0, 0xff0000, 2)
            cvui.update(theWindowName = self.WindowName)
            cv.imshow(self.WindowName,frame)
            c = cv.waitKey(10)
            if c == 27:
                break
            if 48 <= c <= 57 or 97 <= c <= 122 or 65 <= c <= 90 and set == 1:
                text += chr(c)
            if c == 8 and len(text) != 0 and set == 1:
                text = text[0:-1]
            if c == 13 and set == 1:
                msg = '''successfully initialize'''
                tk.messagebox.showinfo(title='tips',message=msg)
                set = 0
            if signin == cur_time:
                web() if choose == 1 else SignIn()
                break
        cv.destroyWindow(winname=self.WindowName)
def web():
    webbrowser.open('https://ke.qq.com/webcourse/index.html?cid=2269340&term_id=102372479#cid=2269340&term_id=102372479&taid=9383159219265692&lite=1')
def SignIn():

    def Click(para):
        win32api.keybd_event(para,0,0,0)
        win32api.keybd_event(para,0,win32con.KEYEVENTF_KEYUP,0) #win32con.KEYEVENTF_KEYUP : 2

    process = '项目管理课程群'
    handle = win32gui.FindWindow('TXGuiFoundation',process)

    # 检查窗口是否最小化，如果是最大化
    if(win32gui.IsIconic(handle)):
        ret = win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
        # ret = win32gui.ShowWindow(handle, win32con.SW_RESTORE)
        time.sleep(2)
    win32gui.SetForegroundWindow(handle)
    for cnt in range(9):
        Click(0x9)
    # Click(32)
def CheckConsole():
    console = win32api.GetConsoleTitle()
    handle= win32gui.FindWindow(0,console)
    win32gui.ShowWindow(handle,0)
    print(handle)
    # 检查窗口是否最小化，如果是最大化
    # if(win32gui.IsIconic(handle)):
    #     ret = win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
    #     # ret = win32gui.ShowWindow(handle, win32con.SW_RESTORE)
    #     time.sleep(2)
    #     print(ret)
    # 关闭窗口
    # handle.close()
if __name__ == '__main__':
    # CheckConsole()
    app = LoginWindow()

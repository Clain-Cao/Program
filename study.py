#coding:utf-8
import cv2 as cv
import numpy as np
import tkinter as tk
import tkinter.messagebox , threading
from PIL import ImageTk, Image
import cvui,time,os,webbrowser,random,datetime
import win32gui,win32api,win32con
from datetime import datetime as D
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
        if self.User.get() == 'admin' and self.password.get() == '123456':
            self.master.destroy()
            MainPage()
        else:
            msg = 'user or  password is error , try again please '
            tk.messagebox.showinfo(title='error',message=msg)
        pass
        # self.master.destroy()
        # MainPage()
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
        Welcome to my world. this Application is designed by me.
        if u wanna use the app. correctly show my Information
        please. thank u very much.
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
        self.SetButton(self.Study,x=600,y=500,width=190,txt='Study Hard')
        # os.system('pause')
    def Back(self):
        self.master.destroy()
        LoginWindow()
    def Capture(self):
        # self.master.destroy()
        ans = tk.messagebox.askyesno(title="tips" , message="are you sure?")
        CapturePage() if ans == True else tk.messagebox.showinfo(title="tips",message="you are correct, ")
        # MainPage()
    def Study(self):
        # self.master,destroy()
        BasicPage()
class CapturePage(object):
    def __init__(self,width=800,height=1200,name='window',BGcolor=(49, 52, 49)):
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
        signin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' (default) '
        text = ''
        set = 0
        while True:
            # frame[:] = self.color
            frame = cv.resize(wallpaper , (self.WindowHeight,self.WindowWidth))
            status , cap = self.capture.read()
            cap = cv.resize(cap,(600,600))
            cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            cvui.printf(frame , 30 ,30, 0.7,0xff0000, "current    time : %s"  , cur_time)
            cvui.printf(frame , 30 ,70, 0.7,0xff0000, "signin     time : %s"  , signin)
            cvui.printf(frame , 30 ,100, 0.7,0xff0000,"computer time : %s"  , int(time.time()))
            if cvui.button(frame, 30, 180, 'Linux Button') == True:
                choose = 1
                signin = '2020-05-20 08:00:00'
                # signin = '2020-05-20 01:46:30' #test

            if cvui.button(frame, 150, 180, 'algebra Button') == True:
                choose = 0
                signin = '2020-05-21 07:58:00'
                # signin = '2020-05-21 01:00:40' #test
            if cvui.button(frame ,300  , 180 , 'set name') == True:
                set = set ^ 1
            cvui.image(frame , 590,10,cap)
            cvui.printf(frame , 30 ,250, 0.7,0xff0000,"your choice : %s"  , 'Linux' if choose == 1 else 'algebra')
            if set == 1:
                cv.putText(frame , 'your name :' + text , (30,300) , cv.FONT_HERSHEY_COMPLEX, 1.0, 0xff0000, 2)
            cvui.update(theWindowName = self.WindowName)
            cv.imshow(self.WindowName,frame)
            c = cv.waitKey(10)

            if int(time.time()) % 1800 == 0:
                '''
                Report On Time
                '''
                ReportOnTime(Time=cur_time)

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
class Listener(object):
    def __init__(self,listenlogs = 'ListenLogs.logs'):
        self.CurTime = time.localtime()
        self.ListenLogs = listenlogs
        self.StartUp()
    def RecordLogs(self,content):
        self.CurTime = time.localtime()
        self.recorder.write(content + '\n')
    def StartUp(self):
        if not os.path.exists(self.ListenLogs):
            with open(self.ListenLogs,'w',encoding='utf-8'):
                pass
        record = open(self.ListenLogs,'a+',encoding='utf-8')
        self.recorder = record
        self.StartTime = time.time()
        self.RecordLogs(content='%s : Listener initialize successfully' % (time.asctime()))
        print('Listener initialize successfully')
    def ShutDown(self):
        self.EndTime = time.time()
        self.RecordLogs(content='%s : You have successfully exited the learning page . This learning time is %s ' % (time.asctime(),datetime.timedelta(seconds = self.EndTime - self.StartTime )) )
        self.recorder.close()

class Frame(object):
    def __init__(self , framename , useBackground = False , coordx=0 , coordy=0 , father=None , background=None , pagewidth=500 , pagelength=1000):
        self.width = pagewidth
        self.length = pagelength
        self.father = father
        self.relx  = coordx # Relative coordinate x in the father frame
        self.rely = coordy # Relative coordinate y in the father frame
        self.useBackground = useBackground
        self.judge(coordx,coordy,framename,background)
    def judge(self,coordx,coordy,framename,background):
        if self.father == None:
            self.x = 0
            self.y = 0
            self.FrameName = framename
            self.background = cv.resize(src=background,dsize=(self.length,self.width))
        else :
            self.FrameName = self.father.FrameName + '/' + framename
            self.x = self.father.x + coordx # Absolute coordinate x
            self.y = self.father.y + coordy # Absolute coordinate y
            if coordx + self.length >= self.father.length :
                raise ValueError(self.FrameName + ' length is too long')
                exit()
            elif coordy + self.width >= self.father.width :
                raise ValueError(self.FrameName + ' width is too long')
                exit()
            if self.useBackground == False:
                self.background = self.father.background[self.rely:self.rely+self.width,self.relx:self.relx+self.length]
            else:
                self.background = cv.resize(src=background,dsize=(self.length,self.width))
        self.OrgBackground = self.background

    def createButton(self,x,y,info):
        status = cvui.button(self.background,x,y,info)
        return status
    def mergeFrame(self):
        if self.father == None:
            print(self.FrameName)
            raise ValueError('%s : FatherNotFoundError' % (self.FrameName))
            return
        cvui.image(self.father.background , self.relx , self.rely,self.background)
    def createPrint(self,y,x,charsize,charcolor,Info,vars):
        cvui.printf(self.background , y ,x, charsize,charcolor, Info,vars)
    def putText(self,info,x,y,charcolor=(255,255,255),charsize=1.0,size=2):
        cv.putText(self.OrgBackground , info , (x,y) , cv.FONT_HERSHEY_COMPLEX, charsize, charcolor, size)
    def text(self,x,y,info,charsize=1,charcolor=0xff0000):
        cvui.text(self.background, y, x, info, charsize, charcolor)
    def UpdateBackground(self,new_bg):
        new_bg = cv.resize(src=new_bg,dsize=(self.length,self.width))
        self.background = new_bg
        self.mergeFrame()
class BasicPage(object):
    def __init__(self , pagewidth=1000 , pagelength=1400 , name = 'Study Window'):
        self.width = pagewidth
        self.length = pagelength
        self.capture = cv.VideoCapture(0)
        self.WindowName = name
        self.Executer = ExecuteStudy()
        self.CreateFrame()
    def CreateFrame(self):
        date = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        months = ['','January','February','March','April','May','June','July','Aguest','September','October','November','December']
        cvui.init(self.WindowName)
        wallpaper = cv.imread('xuejing.jpg')
        cup = cv.imread('cup.jpg')
        self.background = wallpaper
        cv.moveWindow(winname=self.WindowName,x=250,y=0)
        catcher = int(time.time()) + random.randint(2700,5000)
        # catcher = int(time.time()) + random.randint(3,10)
        WARN = '2020-06-12 14:25:00'
        while True:
            Basis = Frame('Basis',background=self.background,pagewidth=self.width, pagelength=self.length)
            Capframe = Frame('Capture',coordx=500,coordy=200,father=Basis,pagewidth=600,pagelength=899)
            # Capframe.createPrint(y=10,x=10,charsize=0.7,charcolor=0xff0000,Info="距离考研还有205天")

            ExamTips = Frame("ExamInfo",coordx=10,coordy=10,father=Basis,pagewidth=190,pagelength=400) # Basis/ExamTips
            ExamTips.putText(x=10,y=30,info="  %d days before " % (self.Executer.DaysRemaining),charcolor=(255,255,255))
            ExamTips.putText(x=10,y=80,info="the graduate exam",charcolor=(255,255,255))


            Sentences = Frame("Motto",coordx=500,coordy=800,father=Basis,pagewidth=189,pagelength=899)
            subMotto11 = '''1. The front is a blind alley , hope in the corner ,'''
            subMotto12 = '''dream in the heart , road in the feet .'''
            Motto2 = '''2. Nothing is impossible'''
            subMotto31 = '''3. Time the study pain is temporary, has not '''
            subMotto32 = '''learned the pain is life-long.'''
            Sentences.putText(x=0,y=30,info=subMotto11,charcolor=(255,255,255))
            Sentences.putText(x=45,y=60,info=subMotto12,charcolor=(255,255,255))
            Sentences.putText(x=0,y=90,info=Motto2,charcolor=(255,255,255))
            Sentences.putText(x=0,y=130,info=subMotto31,charcolor=(255,255,255))
            Sentences.putText(x=45,y=170,info=subMotto32,charcolor=(255,255,255))

            Report = Frame('Report',coordx=500,coordy=20,father=Basis,pagewidth=150,pagelength=899)
            cur_time = time.localtime()
            strtime = time.strftime("%Y-%m-%d %H:%M:%S", cur_time)
            Report.putText(x=30,y=40,info=" Now Time : %s" % strtime,charsize=1.3)
            Report.putText(x=30,y=70,info=' _____________________________________________')
            Report.putText(x=70,y=120,info='      %s ,  %d %s ' % (date[cur_time.tm_wday] , cur_time.tm_mday , months[cur_time.tm_mon] ) , size=4,charsize=1.5 )
            # Sentences.mergeFrame()
            # ExamTips.mergeFrame()
            # Report.mergeFrame()
            ret , frame = self.capture.read()
            # cv.putText(x=10,y=40,info="Now Time : %s " %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            # cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # cv.putText(Basis.background , " Now Time : %s" % cur_time , (500,30) , cv.FONT_HERSHEY_COMPLEX, 1.0, (255,255,255), 2)
            Capframe.UpdateBackground(frame)
            c = cv.waitKey(10)
            if cur_time.tm_hour % 24 == 0 and cur_time.tm_min % 60 == 0:
                self.Executer.UpdateDays()
            if catcher <= int(time.time()):

                if not os.path.exists('Status'):
                    os.mkdir('Status')

                if not os.path.exists('Status/' + months[cur_time.tm_mon]):
                    os.mkdir('Status/' + months[cur_time.tm_mon] + '/' )

                if not os.path.exists('Status/' + months[cur_time.tm_mon] + '/' + str(cur_time.tm_mday)):
                    os.mkdir('Status/' + months[cur_time.tm_mon] + '/' + str(cur_time.tm_mday))

                cv.imwrite('Status/' + months[cur_time.tm_mon] + '/' + str(cur_time.tm_mday) + '/%s.bmp' % time.strftime("%Y-%m-%d %H-%M-%S", cur_time) ,Basis.background)
                catcher = int(time.time()) + random.randint(3600,5000)
                print('触发监听器')
                self.Executer.listener.RecordLogs(content='%s : The program has successfully catched a photo' % strtime )
            if WARN == strtime:
                tk.messagebox.showinfo(title="tips",message='class will begin as soon as possible')
            if c == 27:
                ans = tk.messagebox.askyesno(title="tips" , message="are you sure?")
                if ans == True:
                    self.Executer.listener.ShutDown()
                    break
                else :
                    continue
            cvui.update(theWindowName = self.WindowName)
            cv.imshow(self.WindowName,Basis.background)
        cv.destroyWindow(winname=self.WindowName)


class ExecuteStudy(object):
    def __init__(self,LogPath='study.log', images_logs='Attitude'):
        self.Logs = LogPath
        self.Days = {}
        self.ImagesLogs = images_logs
        self.StudyTime = 0
        self.LastExitTime = 0
        self.DaysRemaining = 200
        self.listener = Listener()
        self.Init()
    def Init(self):
        try:
            with open(self.Logs,'r',encoding='utf-8') as f:
                cnt = 1
                line = (f.readline()).replace("\n","")
                while line != '':
                    if cnt == 1:
                        line = line.splits('/')
                        self.DayNumber = int(line[0])
                        line.pop(0) # del(line[0])
                        for day in line:
                            day = day.splits('+')
                            self.Days.update({day[0] : day[1]})  # date : time
                    elif cnt == 2:
                        self.DaysRemaining = int(line)
                    else :
                        self.LastExitTime = line
                    line = (f.readline()).replace("\n","")
                    cnt += 1
        except :
            with open(self.Logs,'w',encoding='utf-8') as f:
                pass
        self.UpdateDays()
        tk.messagebox.showinfo(title='tips',message='initialize successfully')
        self.listener.RecordLogs(content='%s : You have successfully logged into the interface' % ( time.strftime("%Y-%m-%d %H:%M:%S", self.listener.CurTime)))
    # def DataSaver():
    #     with open(self.Logs,'w',encoding='utf-8') as f:
    #         f.write(self.)
    #     pass
    def UpdateDays(self):
        future = D.strptime('2020-12-21 00:00:00','%Y-%m-%d %H:%M:%S')
        now = D.now()
        delta = future - now
        self.DaysRemaining = delta.days + 1
def ReportOnTime(Time):
    msg = 'currnet time is '
    winname = 'Tips'
    tk.messagebox.showinfo(winname,message=msg + Time)
    handle = win32gui.FindWindow(None,'MainPage')
    if(win32gui.IsIconic(handle)):
        ret = win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
        # ret = win32gui.ShowWindow(handle, win32con.SW_RESTORE)
    # win32gui.SetForegroundWindow(handle)
    time.sleep(1)
def web():
    webbrowser.open('https://ke.qq.com/webcourse/index.html?cid=2269340&term_id=102372479#cid=2269340&term_id=102372479&taid=9383159219265692&lite=1')
def algebra():
    webbrowser.open('https://www.bilibili.com/video/BV15C4y1W7na?p=5')
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
    Click(32)
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
    CheckConsole()
    app = LoginWindow()

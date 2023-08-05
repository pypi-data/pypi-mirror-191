from tkinter import *
import time
from threading import Thread

class CPS:
    def __init__ (self):
        self.cps = 0
        self.clicks = 0
        self.time_sec = 0
        
        self.window = Tk()

        self.window.geometry("600x450+660+210")
        self.window.resizable(False,  False)
        self.window.title("PyCPS")
        self.window.configure(background="#d9d9d9")
           
        self.Clicks_l = Label(self.window)
        self.Clicks_l.place(relx=0.05, rely=0.067, height=21, width=34)
        self.Clicks_l.configure(background="#d9d9d9")
        self.Clicks_l.configure(compound='left')
        self.Clicks_l.configure(disabledforeground="#a3a3a3")
        self.Clicks_l.configure(text='''0''')
        self.Label2 = Label(self.window)
        self.Label2.place(relx=0.133, rely=0.067, height=21, width=34)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(text='''clicks''')
        self.Button1 = Button(self.window)
        self.Button1.place(relx=0.05, rely=0.178, height=194, width=547)
        self.Button1.configure(activebackground="beige")
        self.Button1.configure(activeforeground="black")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(text='''Click here to get started''')
        self.Button1.configure(command = self.__Button1Function)
        self.Time_l = Label(self.window)
        self.Time_l.place(relx=0.383, rely=0.067, height=21, width=34)
        self.Time_l.configure(background="#d9d9d9")
        self.Time_l.configure(text='''0''')
        self.Label4 = Label(self.window)
        self.Label4.place(relx=0.5, rely=0.067, height=21, width=34)
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(compound='left')
        self.Label4.configure(text='''time''')
        self.cps_l = Label(self.window)
        self.cps_l.place(relx=0.75, rely=0.067, height=21, width=34)
        self.cps_l.configure(background="#d9d9d9")
        self.cps_l.configure(text='''0''')
        self.Label6 = Label(self.window)
        self.Label6.place(relx=0.833, rely=0.067, height=21, width=34)
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(text='''cps''')
        self.Button2 = Button(self.window)
        self.Button2.place(relx=0.05, rely=0.644, height=54, width=547)
        self.Button2.configure(activebackground="beige")
        self.Button2.configure(activeforeground="black")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(text='''Click here to start the timer''')
        self.Button2.configure(command = self.__Button2Function)

        self.window.mainloop()

        
    def __click_count (self):
        self.clicks += 1
        self.Clicks_l["text"] = self.clicks

    def __timer (self):
        while self.time_sec:
            mins, secs = divmod(self.time_sec, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            self.time_sec -= 1
            self.Time_l ["text"] = self.time_sec
            
            if self.Time_l["text"] == 0:
                self.cps = self.clicks / 10
                self.cps_l["text"] = self.cps
                
    def __Button1Function (self):
        Thread (target = self.__click_count).start()
        
    def __Button2Function (self):
        self.clicks = 0
        self.cps = 0
        self.time_sec = 10
        Thread (target = self.__timer).start()
        
    def getCPS(self):
        return self.cps


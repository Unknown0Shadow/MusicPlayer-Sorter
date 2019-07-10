from controler.controller import Controller
from repository.repository import Repository
from ui.gui import *

f = open("configuration.ini", "r")
bg, fg, pic, version = f.readline().split(" ")
f.close()

r = Repository(int(version))
c = Controller(r)

root = Tk()

root["bg"] = "#000000"

a = TKINTER(c, root, bg, fg, pic)
a.globalConfig()
root.mainloop()

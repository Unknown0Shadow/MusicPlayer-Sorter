from domain.checkbutton import *
from pygame import mixer
from mutagen.mp3 import MP3
from os import getlogin

# Daniel Markovnikov // Unknown0Shadow


class TKINTER:
    def __init__(self, ctrl, root, bg, fg, pic):
        """builds the graphic interface"""
        self.__bg = bg
        self.__fg = fg
        self.__pic = pic
        self.root = root
        self.__ctrl = ctrl
        self.__buttons = Label(self.root)
        self.__buttons.pack(side=TOP)
        self.__search = Frame(self.root)
        self.__search.pack(side=LEFT, fill=BOTH, expand=1)
        Grid.rowconfigure(self.__search, 0, weight=1)
        Grid.columnconfigure(self.__search, 2, weight=1)
        self.__vsb = Scrollbar(self.__search, orient="vertical", command=self.OnVsb)
        self.__vsb.grid(row=0, column=0, sticky=N + S)
        self.__nr = Listbox(self.__search, width=4, yscrollcommand=self.yscroll2)
        self.__nr.grid(row=0, column=1, sticky=N + S)
        self.__lab = Listbox(self.__search, yscrollcommand=self.yscroll1)
        self.__lab.bind('<<ListboxSelect>>', self.curSelect)
        self.__lab.grid(row=0, column=2, sticky=N + S + E + W)
        self.__checks = Label()
        self.__checks.grid(in_=self.__search, row=0, column=3, sticky=N+S)

        self.__buttonCollection = []
        tags = self.getCategories()
        for i in range(0, len(tags)):
            self.__buttonCollection.append(CB(self.__checks, tags[i], i, 0))

        self.b23 = Button(self.__checks, text='Search', command=self.findByElements, state="disabled", width=20)
        self.b23.grid(row=22, column=0)
        self.b24 = Button(self.__checks, text="Edit", command=self.cmd_b24, state="disabled", width=20)
        self.b24.grid(row=23, column=0)

        self.__ent = Entry(self.__search, width=22)
        self.__ent.grid(row=1, column=3, sticky=E)
        self.__text = Label(self.__search, text="")
        self.__text.grid(row=1, column=2, sticky=E)
        self.__playtime = Label(self.__search, text="")
        self.__playtime.grid(row=1, column=1, sticky=E)
        self.__Button1 = Button(self.__buttons, text="Find By Element", command=self.findByElement, width=15)
        self.__Button1.pack(side=LEFT)
        self.__Button2 = Button(self.__buttons, text="Find By Title", command=self.findByTitle, width=15)
        self.__Button2.pack(side=LEFT)
        self.__Button3 = Button(self.__buttons, text="Find By Score", command=self.findByScore, width=15)
        self.__Button3.pack(side=LEFT)
        self.__Button4 = Button(self.__buttons, text="Add Elements", command=self.addElements, state="disabled", width=15)
        self.__Button4.pack(side=LEFT)
        self.__Button5 = Button(self.__buttons, text="Play Current", command=self.play, state="disabled", width=15)
        self.__Button5.pack(side=LEFT)
        self.__Button6 = Button(self.__buttons, text="Pause Current", command=self.pause, state="disabled", width=15)
        self.__Button6.pack(side=LEFT)
        self.__loadButton = Button(self.__buttons, text="Load", command=self.loadFile, width=15)
        self.__loadButton.pack(side=LEFT)
        self.__saveButton = Button(self.__buttons, text="Save",  command=self.save, width=15)
        self.__saveButton.pack(side=LEFT)
        self.__quitButton = Button(self.__buttons, text="Exit",  command=self.quit, width=15)
        self.__quitButton.pack(side=LEFT)

        menu = Menu(root)
        root.config(menu=menu)
        menu.add_command(label="Help", command=self.help)
        styleMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Style", menu=styleMenu)
        styleMenu.add_command(label="Red", command=self.configRed)
        styleMenu.add_separator()
        styleMenu.add_command(label="Orange", command=self.configOrange)
        styleMenu.add_separator()
        styleMenu.add_command(label="Yellow", command=self.configYellow)
        styleMenu.add_separator()
        styleMenu.add_command(label="Green", command=self.configGreen)
        styleMenu.add_separator()
        styleMenu.add_command(label="Cyan", command=self.configCyan)
        styleMenu.add_separator()
        styleMenu.add_command(label="Blue", command=self.configBlue)
        styleMenu.add_separator()
        styleMenu.add_command(label="Magenta", command=self.configMagenta)
        styleMenu.add_separator()
        styleMenu.add_command(label="Disk", command=self.configDisk)

        self.loadMenu = Menu(menu, tearoff=False)
        menu.add_cascade(label="Load", menu=self.loadMenu)
        [self.loadMenu.add_command(label=file, command=lambda text=file: self.loadThis(text))
         for file in self.__ctrl.getAllFiles()]
        # for file in self.__ctrl.getAllFiles():
        #     self.loadMenu.add_command(label=file, command=lambda text=file: self.loadThis(text))
        menu.add_cascade(label="Style", menu=styleMenu)
        menu.add_command(label="Bands", command=self.getBands)

        imgicon = PhotoImage(file=self.__pic)
        self.root.tk.call('wm', 'iconphoto', self.root._w, imgicon)
        self.root.title("HEAL PROJECT - MUSIC")
        self.root.bind("<Button-1>", self.rootFocus)
        self.root.bind("<p>", self.pause)
        self.root.bind("<g>", self.play)
        self.root.bind("<e>", self.cmd_b24)
        self.root.bind("<s>", self.findByElements)
        self.root.bind("<Escape>", self.quit)
        self.root.bind("<F1>", self.help)

        self.thing = ""
        self.__command = ""
        self.__entCommand = ""
        self.__saved = True
        self.__list = []
        self.__value = ""
        self.__whitespace = True
        self.__paused = False
        self.__pausable = False
        self.__playing = ""
        self.__duration = 0
        self.__arguments = []
        self.__bigButtons = [self.__Button1, self.__Button2, self.__Button3, self.__quitButton, self.__saveButton, self.__loadButton]
        #self.__buttonCollection = [self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9, self.b10, self.b11, self.b12, self.b13, self.b14, self.b15, self.b16, self.b17, self.b18, self.b19, self.b20, self.b21, self.b22]

    def help(self, event=None):
        messagebox.showinfo("Help - Commands", "Use the key <P> to pause or unpause music, while playing of course.\nUse the key <G> to start playing a selected song.\nUse the key <E> to set the checkbox label for editing.\nUse the key <S> to set the checkbox label for searching.\n<Double-Mouse1> on a band to display all songs.\nUse <Return> (also known as Enter) to use the activated option, either editing the elements of a song, either seeking songs by selected elements.\nUse the key <F1> to see the help menu (this which you are reading right now).\nNote! Do not use <Shift> and key at the same time, will not work.\nUse the key <Esc> to close the program.")

    def getBands(self):
        bands = sorted(set([title.split(" - ")[0] for title in self.__ctrl.findByTitle("")]))
        self.adder(bands, "bands")

    def globalConfig(self):
        """configures the style"""
        self.__buttons.config(bg=self.__bg)
        self.__search.config(bg=self.__bg)
        imgicon = PhotoImage(file=self.__pic)
        self.root.tk.call('wm', 'iconphoto', self.root._w, imgicon)
        # for thing in (self.__Button1, self.__Button2, self.__Button3, self.__Button4, self.__Button5, self.__Button6, self.__playtime, self.__loadButton, self.__saveButton, self.__quitButton, self.__nr, self.__lab, self.__ent, self.__text):
        #     thing.config(bg=self.__bg, fg=self.__fg)
        [thing.config(bg=self.__bg, fg=self.__fg) for thing in (self.__Button1, self.__Button2, self.__Button3, self.__Button4, self.__Button5, self.__Button6, self.__playtime, self.__loadButton, self.__saveButton, self.__quitButton, self.__nr, self.__lab, self.__ent, self.__text)]

    def configGreen(self):
        """configures the style"""
        self.__bg = "black"
        self.__fg = "#00F00D"
        self.__pic = "Green.gif"
        self.__ctrl.config(self.__bg, self.__fg, self.__pic)
        self.globalConfig()

    def configRed(dm):
        """configures the style"""
        dm.__bg = "black"
        dm.__fg = "red"
        dm.__pic = "Red.gif"
        dm.__ctrl.config(dm.__bg, dm.__fg, dm.__pic)
        dm.globalConfig()

    def configOrange(dm):
        """configures the style"""
        dm.__bg = "black"
        dm.__fg = "#ffa500"
        dm.__pic = "Orange.gif"
        dm.__ctrl.config(dm.__bg, dm.__fg, dm.__pic)
        dm.globalConfig()

    def configCyan(self):
        """configures the style"""
        self.__bg = "black"
        self.__fg = "#00FFFF"
        self.__pic = "Cyan.gif"
        self.__ctrl.config(self.__bg, self.__fg, self.__pic)
        self.globalConfig()

    def configBlue(self):
        """configures the style"""
        self.__bg = "black"
        self.__fg = "#0000FF"
        self.__pic = "Blue.gif"
        self.__ctrl.config(self.__bg, self.__fg, self.__pic)
        self.globalConfig()

    def configMagenta(self):
        """configures the style"""
        self.__bg = "black"
        self.__fg = "#FF00FF"
        self.__pic = "Magenta.gif"
        self.__ctrl.config(self.__bg, self.__fg, self.__pic)
        self.globalConfig()

    def configYellow(self):
        """configures the style"""
        self.__bg = "black"
        self.__fg = "#FFFF00"
        self.__pic = "Yellow.gif"
        self.__ctrl.config(self.__bg, self.__fg, self.__pic)
        self.globalConfig()

    def configDisk(self):
        """configures the style"""
        self.__bg = "black"
        self.__fg = "#FFFFFF"
        self.__pic = "Disk.gif"
        self.__ctrl.config(self.__bg, self.__fg, self.__pic)
        self.globalConfig()

    def OnVsb(self, *args):
        """Fixes the scrolling option"""
        self.__lab.yview(*args)
        self.__nr.yview(*args)

    def yscroll1(self, *args):
        """Fixes the scrolling option"""
        if self.__nr.yview() != self.__lab.yview():
            self.__nr.yview_moveto(args[0])
        self.__vsb.set(*args)

    def yscroll2(self, *args):
        """Fixes the scrolling option"""
        if self.__lab.yview() != self.__nr.yview():
            self.__lab.yview_moveto(args[0])
        self.__vsb.set(*args)

    def cmd_b24(self, event=None):
        """prepares the checkbuttons for editing arguments to a song"""
        if len(self.__lab.get(0, END)) != 0:
            self.__command = "edit"
            self.b23.config(state="normal")
            self.b24.config(state="disabled")

    def savelist(self, event):
        """saves the changes made in checkbox label"""
        if self.__value != "":
            try:
                self.__saved = False
                for button in self.__buttonCollection:
                    if button.var.get():
                        if button.title() == "#L" or button.title() == "#T" or button.title() == "#I" or button.title() == "IMPORTANT":
                            self.__arguments.append(button.title())
                        else:
                            self.__arguments.append(button.title().lower())
                text = ""
                counter = 0
                for el in self.__arguments:
                    if counter > 0:
                        text += ", "
                    text += el
                    counter += 1
                self.__ctrl.replace(self.__value, self.__arguments)
                self.__arguments = []  # clean
                try:
                    a = self.__lab.get(0, END).index(self.song)
                    self.__lab.delete(a)
                    self.song = self.__value + ":  " + text
                    self.__lab.insert(a, self.song)
                except:
                    self.findByScore()
                    for el in self.__list:
                        if el[0] == self.__value:
                            a = self.__lab.get(0, END).index(el[0]+" = "+str(el[1]))
                            break
                finally:
                    self.__lab.selection_set(a)
                    self.__lab.activate(a)
            except:
                return

    def rootFocus(self, event):
        try:
            focused = self.root.focus_get()
            if focused == self.__ent:
                self.root.unbind("<p>")
                self.root.unbind("<g>")
                self.root.unbind("<e>")
                self.root.unbind("<s>")
                self.root.unbind("<Return>")
                self.root.unbind("<Escape>")
                if self.__entCommand == "element":
                    self.__ent.bind("<Return>", self.findByElement_D)
                elif self.__entCommand == "title":
                    self.__ent.bind("<Return>", self.findByTitle_D)
                elif self.__entCommand == "add":
                    self.__ent.bind("<Return>", self.add)
                elif self.__entCommand == "saveError":
                    self.__ent.bind("<Return>", self.savedError_D)
                elif self.__entCommand == "load":
                    self.__ent.bind("<Return>", self.loadFile_D)
            else:
                self.__ent.unbind("<Return>")
                self.root.bind("<p>", self.pause)
                self.root.bind("<g>", self.play)
                self.root.bind("<e>", self.cmd_b24)
                self.root.bind("<s>", self.findByElements)
                self.root.bind("<Escape>", self.quit)
                self.root.bind("<Escape>")
                if self.__command == "search":
                    self.root.bind("<Return>", self.findByElements_D)
                elif self.__command == "edit":
                    self.root.bind("<Return>", self.savelist)
        except:
            return

    def findByBand(self, event):
        try:
            self.__ent.delete(0, END)
            self.__ent.insert(END, self.__value)
            self.findByTitle_D(event)
        except:
            return

    def curSelect(self, event):
        """Allows to select with the mouse cursor songs shown on the screen, for further usage"""
        try:
            self.__value = str((self.__lab.get(self.__lab.curselection())))
            try:
                self.__value, _ = self.__value.split(":")
            except:
                self.__value, _ = self.__value.split(" =")
            self.song = self.__ctrl.findSpecific(self.__value)
            _, arguments = self.song.split(":  ")
            self.__Button4.config(state="normal")
            self.__Button5.config(state="normal")
            try:
                self.__arguments = arguments.lower().split(", ")
            except: self.__arguments.append(arguments.lower())

            for button in self.__buttonCollection:
                if button.title().lower() in self.__arguments:
                    button.var.set(True)
                else: button.var.set(False)
            self.__arguments = []
        except:
            self.__Button4.config(state="disabled")
            self.__Button5.config(state="disabled")

    def changeLabel(self):
        """Displays the time left until the song ends"""
        if mixer.music.get_busy():
            self.__playtime.config(text=(int(self.__duration) - int(mixer.music.get_pos() // 1000)))
            self.root.after(1000, self.changeLabel)
        else:
            self.__pausable = False
            self.__Button6.config(state="disabled")

    def getDuration(self):
        """Gets the length of the song"""
        self.audio = MP3(self.__playing)
        self.__duration = self.audio.info.length

    def play(self, event=None):
        """Plays a selected song from the screen"""
        try:
            self.__playing = "C:/Users/{}/Music/".format(getlogin()) + self.__value + ".mp3"
            self.getDuration()
            if mixer.get_init():
                mixer.quit()
            mixer.init(frequency=self.audio.info.sample_rate)
            mixer.music.load(self.__playing)
            mixer.music.play()
            self.changeLabel()
            self.__paused = False
            self.__pausable = True
            self.__Button6.config(state="normal")
        except:
            self.__Button6.config(state="disabled")

    def pause(self, event=None):
        """Simply pauses the music"""
        if self.__pausable:
            if self.__paused:
                mixer.music.unpause()
            else:
                mixer.music.pause()
            self.__paused = not self.__paused

    def findByElements(self, event=None):
        """prepares checkbuttons for searching songs"""
        if len(self.__lab.get(0, END)) != 0:
            self.b23.config(state="disabled")
            self.b24.config(state="normal")
            self.__command = "search"

    def findByElements_D(self, event):
        """seeks songs by multiple elements checked"""
        for button in self.__buttonCollection:
            if button.var.get():
                if button.title() == "#L" or button.title() == "#T" or button.title() == "#I" or button.title() == "IMPORTANT":
                    self.__arguments.append(button.title())
                else:
                    self.__arguments.append(button.title().lower())
        self.__list = self.__ctrl.findByTitle("")
        for element in self.__arguments:
            self.__list = self.__ctrl.findByElementInList(element, self.__list)
        self.__arguments = []  # clean
        self.adder()

    def findByElement(self):
        """Sets the entry box ready for seeking songs by element"""
        self.__entCommand = "element"
        self.__ent.delete(0, END)
        self.__ent.insert(END, "Enter element")
        self.__text.config(text="Enter element:  ")

    def findByElement_D(self, event):
        """
        Seeks through the dictionary '__stats' songs that contain the tag 'element' given as parameter to the Controller module.
        """
        self.__list = self.__ctrl.findByElement(self.__ent.get())
        self.adder()

    def findByTitle(self):
        """Sets the entry box ready for seeking songs by title"""
        self.__entCommand = "title"
        self.__ent.delete(0, END)
        self.__ent.insert(END, "Enter title")
        self.__text.config(text="Enter title:  ")

    def findByTitle_D(self, event):
        """
        Seeks through the dictionary '__stats' songs that contain the name 'title' given as parameter to the Controller module. The 'title' can also be an incomplete song name, and if there are any songs that contain it, they will be selected.
        """
        self.__list = self.__ctrl.findByTitle(self.__ent.get())
        self.adder()

    def findByScore(self):
        """
        Calculates the score of the tags of each song, and returns a 2 dimensional list, first element is the song name, the second is the tags sum.
        """
        self.__lab.delete(0, END)
        self.__nr.delete(0, END)
        stuff = self.__ctrl.findByScore(self.__list)
        items = []
        [items.append(el[0] + " = " + str(el[1])) for el in stuff]
        # for el in stuff:
        #     items.append(el[0] + " = " + str(el[1]))
        self.adder(items)

    def addElements(self):
        """Sets the entry box ready for adding elements"""
        self.__ent.delete(0, END)
        self.__entCommand = "add"
        self.__ent.insert(END, "Enter element")
        self.__text.config(text="Enter element to add:  ")
        self.__saved = False
        self.__lab.delete(0, END)
        self.__nr.delete(0, END)
        _, arguments = self.song.split(":")
        if len(arguments) <= 2:
            self.__whitespace = True
        else:
            self.__whitespace = False
        self.__lab.insert(END, self.song)
        self.__nr.insert(END, "---")

    def add(self, event):
        """
        Simply checks if an element given as parameter to the Controller module is allowed to be set as a tag for the song, which referred by title, then it adds it if valid.
        """
        element = self.__ent.get()
        text = self.__ctrl.add(self.__value, element)
        element = " "+element
        self.__text.config(text=text+"  ")
        if text == "Enter element to add:  ":
            if self.__whitespace:
                self.__whitespace = False
            else:
                element = ","+element
            element = self.__lab.get(0)+element
            self.__lab.delete(0)
            self.__lab.insert(0, element)
            self.__ent.delete(0, END)

    def save(self):
        """
        Saves the information from the dictionary '__stats' into a file named with the version plus Heal.file.
        """
        self.__list = self.__lab.get(0, END)
        self.__lab.delete(0, END)
        self.__nr.delete(0, END)
        self.__ent.delete(0, END)
        text = self.__text.cget("text")
        self.root.after(100, lambda: self.__text.config(text="Saving... "))
        self.__ctrl.save()
        self.root.after(1000, lambda: self.__text.config(text="Saved... "))
        self.__saved = True
        self.root.after(1900, lambda: self.__text.config(text=text))
        self.allButtons("disabled")
        self.__Button4.config(state="disabled")
        self.__Button5.config(state="disabled")
        self.__Button6.config(state="disabled")
        [button.config("state", "disabled") for button in self.__buttonCollection]
        # for button in self.__buttonCollection:
        # #dm button.config("state", "disabled")
        self.root.after(2000, lambda: self.allButtons("normal"))
        self.root.after(2000, lambda: self.adder())
        if self.__pausable:
            self.root.after(2000, lambda: self.__Button6.config(state="normal"))
        self.loadMenu.delete(0, END)
        [self.loadMenu.add_command(label=file, command=lambda text=file: self.loadThis(text))
         for file in self.__ctrl.getAllFiles()]
        # for file in self.__ctrl.getAllFiles():
        #     self.loadMenu.add_command(label=file, command=lambda text=file: self.loadThis(text))

    def allButtons(self, action):
        """Enables or disables all buttons"""
        if action == "normal" or action == "disabled":
            # for button in self.__buttonCollection:
            #     button.config("state", action)
            [button.config("state", action) for button in self.__buttonCollection]
            # for button in self.__bigButtons:
            #     button.config(state=action)
            [button.config(state=action) for button in self.__bigButtons]

    def quit(self, event=None):
        """Closes the Graphic User Interface"""
        if self.__saved:
            self.__lab.delete(0, END)
            self.__nr.delete(0, END)
            self.__ent.delete(0, END)
            self.__text.config(text="Quiting...  ")
            self.root.after(1000, lambda: self.root.quit())
        else:
            self.thing = "quit"
            self.savedError()

    def adder(self, items=None, option="songs"):
        """
        Adds elements from a list to the screen, used to shorten a couple of functions, some functions required multiple instructions during this process so they didn't use this function.
        """
        if items is None:
            items = self.__list
        self.__value = ""
        self.__lab.delete(0, END)
        self.__nr.delete(0, END)
        i = 1
        for el in items:
            self.__lab.insert(END, el)
            self.__nr.insert(END, i)
            i += 1
        if len(self.__lab.get(0, END)) == 0 or option == "bands":
            self.b23.config(state="normal")
            self.b24.config(state="disabled")
            self.root.unbind("<e>")
            self.root.unbind("<Return>")
            self.__lab.unbind("<Double-Button-1>")
        if option == "bands":
            self.__lab.bind("<Double-Button-1>", self.findByBand)
        else:
            self.__lab.unbind("<Double-Button-1>")

    def loadFile(self):
        """Sets the entry box ready for loading file"""
        if self.__saved:
            self.__entCommand = "load"
            self.__ent.delete(0, END)
            self.__ent.insert(END, "Enter file name")
            self.__text.config(text="Enter file name:  ")
        else:
            self.thing = "load"
            self.savedError()

    def loadFile_D(self, event):
        """Simply loads the resources from a file, filling the dictionary '__stats'."""
        filename = self.__ent.get()
        text = self.__ctrl.loadFile(filename)
        self.__list = self.__ctrl.findByTitle("")
        self.adder()
        self.__text.config(text=text)
        if self.__command == "":
            self.b23.config(state="normal")
            self.b24.config(state="normal")
        self.__value = ""
        self.root.unbind("<Return>")
        self.__ent.unbind("<Return>")
        self.__ent.delete(0, END)
        # for button in self.__buttonCollection:
        #     button.config("state", "normal")
        [button.config("state", "normal") for button in self.__buttonCollection]

    def loadThis(self, file):
        if self.__saved:
            text = self.__ctrl.loadFile(file)
            self.__list = self.__ctrl.findByTitle("")
            self.adder()
            self.__text.config(text=text)
            if self.__command == "":
                self.b23.config(state="normal")
                self.b24.config(state="normal")
            self.__value = ""
            self.root.unbind("<Return>")
            self.__ent.unbind("<Return>")
            self.__ent.delete(0, END)
            for button in self.__buttonCollection:
                button.config("state", "normal")
        else:
            self.thing = "load"
            self.savedError()

    def savedError(self):
        """Sets the entry box ready for confirmation."""
        self.__text.config(text="The progress isn't saved. Proceed?  ")
        self.__entCommand = "saveError"
        self.__ent.delete(0, END)
        self.__ent.insert(END, "1 / 0")

    def savedError_D(self, event):
        """
        If not saved and want to proceed a dangerous operation, this will make sure that the user REALLY wants to proceed that operation without saving.
        """
        answer = self.__ent.get()
        if answer == '1':
            self.__saved = True
            if self.thing == "load":
                self.loadFile()
            elif self.thing == "quit":
                self.quit()
        else:
            self.__entCommand = ""
            self.__ent.unbind("<Return>")
            self.__text.config(text="Returning...  ")

    def getCategories(self):
        return self.__ctrl.getCategories()

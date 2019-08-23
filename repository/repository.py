from os import listdir, getlogin


class Repository:
    def __init__(self, version):
        """
        Constructor:
        '__stats' is a dictionary which contains song names and the elements by which the songs are described.
        '__categories' is a list of words that are allowed to set as categories for the songs.
        """
        self.__stats = {}
        self.__categories = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10", "tag11", "tag12", "tag13", "tag14", "tag15", "tag16", "tag17", "tag18", "tag19", "tag20", "tag21", "tag22"]
        self.version = version

        self.path_global = r"C:\Users\{}\Music".format(getlogin())
        self.song_list = []

    def searchFiles(self, path):
        """Loops through directories within a given path for mp3 files."""
        for file in listdir(path):
            if file == "iTunes":
                continue
            try:
                self.searchFiles(path+"\{}".format(file))
            except:
                if file.endswith(".mp3"):
                    self.song_list.append(file)

    def getAllStats(self):
        """Returns the dictionary of songs and their tags."""
        return self.__stats

    def getCategories(self):
        """Returns the list of possible categories."""
        return self.__categories

    def loadFile(self, filename):
        """Simply loads the resources from a file, filling the dictionary '__stats'."""
        self.checker(filename)
        text = ''
        self.__stats.clear()
        try:
            f = open(filename, "rb")
            lines = f.readlines()
            for element in lines:
                text = text + str(element.decode("utf-8"))
            f.close()
            for line in text.split("\n"):
                if line == "": continue
                name, element = line.split(" ##")
                if name not in self.__stats.keys():
                    self.__stats[name] = element
            return "Loaded "+filename+"  "
        except:
            return "No such file. ERROR  "

    def getAllFiles(self):
        """Returns a list of file names"""
        files = []
        [files.append(file) for file in listdir(".") if file.endswith(".file")]
        # for file in listdir("."):
        #     if file.endswith(".file"):
        #         files.append(file)
        if len(files) == 0:
            f = open("Heal.file", "w")
            f.write("test ## test")
            f.close()
            files.append("Heal.file")
        return files

    def checker(self, filename):
        """Compares the saved file with the music folder"""
        file_melodies = []
        file_names = []
        my_melodies = []
        self.searchFiles(self.path_global)
        for file in self.song_list:
            file, _ = file.split(".m")
            my_melodies.append(file)
        self.song_list.clear()
        f = open(filename, "rb")
        lines = f.readlines()
        f.close()
        for line in lines:
            melody = line.decode("utf-8").replace("\n", "")
            file_melodies.append(melody)
            name, _ = melody.split(" ## ")
            file_names.append(name)
        for mel in file_melodies:
            name, _ = mel.split(" ## ")
            if name not in my_melodies:
                file_melodies.remove(mel)
        if len(file_melodies) != len(my_melodies):
            for mel in my_melodies:
                if mel not in file_names:
                    file_melodies.append(mel + " ## ")
        file_melodies.sort()
        f = open(filename, "wb")
        #f.write("test ## test\n")
        [f.write((mel + "\n").encode("utf-8")) for mel in file_melodies]
        # for mel in file_melodies:
        #     f.write((mel + "\n").encode("utf-8"))
        f.close()

    def add(self, title, element):
        """
        Simply checks if an element given as parameter is allowed to be set as a tag for the song, which referred by title, then it adds it if valid.
        """
        # if element not in self.__categories:
        #     return (str(element) + " is not in categories...")
        if self.__stats[title] == " ":
            self.__stats[title] += element
        else:
            self.__stats[title] += (", " + element)
        return "Enter element to add:  "

    def replace(self, title, arguments):
        """deletes all the argumets then adds the new ones"""
        self.__stats[title] = " "
        for arg in arguments:
            self.add(title, arg)

    def save(self):
        """
        Saves the information from the dictionary '__stats' into a file named with the version plus Heal.file.
        """
        text = ''
        # self.version += 1
        for el in self.__stats:
            if el == "": continue
            text += (el + " ##" + self.__stats[el] + "\n")
        f = open(str(self.version) + "Heal.file", "wb")
        f.write(text.encode("utf-8"))
        f.close()
        # f = open("configuration.ini", "r")
        # text = f.readline().split(" ")
        # f.close()
        # text[3] = str(self.version)
        # f = open("configuration.ini", "w")
        # f.write(text[0]+" "+text[1]+" "+text[2]+" "+str(text[3]))
        # f.close()

    def config(self, bg, fg, pic):
        """saves the new app configuration style in a file"""
        f = open("configuration.ini", "w")
        f.write(bg+" "+fg+" "+pic+" "+str(self.version))
        f.close()

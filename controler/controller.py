class Controller:
    def __init__(self, repo):
        """
        '__repo' refers to the module Repository.
        '__stats' is the dictionary from the module Repository, which contains the name of the songs and their tags.
        :param Repository: Module:Repository.
        """
        self.__repo = repo
        self.__stats = self.__repo.getAllStats()

    def config(self, bg, fg, pic):
        """saves the new app configuration style in a file"""
        self.__repo.config(bg, fg, pic)

    def getCategories(self):
        return self.__repo.getCategories()

    def findSpecific(self, title):
        """returns the representation of song, considering the entire title was writen correctly"""
        return (title + ": " + self.__stats[title])

    def findByElement(self, element):
        """
        Seeks through the dictionary '__stats' songs that contain the tag 'element' given as parameter.
        :param element: tag.
        :return: list of songs that contain the given tag
        """
        stuff = []
        [stuff.append(name + ": " + self.__stats[name]) for name, elements in self.__stats.items()
         if element in elements]
        # for name, elements in self.__stats.items():
        #     #if name == "ï»¿test": continue
        #     if element in elements:
        #         stuff.append(name + ": " + self.__stats[name])
        return stuff

    def findByElementInList(self, element, list_of):
        """
        does the same thing as findByElement except it searches on a given list, not on the dictionary '__stats'
        """
        temp_list = []
        for el in list_of:
            _, arguments = el.split(":")
            if element in arguments:
                temp_list.append(el)
        return temp_list

    def findByTitle(self, title):
        """
        Seeks through the dictionary '__stats' songs that contain the name 'title' given as parameter. The 'title' can also be an incomplete song name, and if there are any songs that contain it, they will be selected.
        :param title: the title of the song
        :return: list of songs that contain the given name
        """
        stats = []
        [stats.append(name + ": " + self.__stats[name]) for name in self.__stats.keys()
         if title.lower() in name.lower()]
        # for name in self.__stats.keys():
        #     #if name == "ï»¿test": continue
        #     if title.lower() in name.lower():
        #         stats.append(name + ": " + self.__stats[name])
        return stats

    def loadFile(self, filename):
        """Simply loads the resources from a file, filling the dictionary '__stats'."""
        text = self.__repo.loadFile(filename)
        return text

    def getAllFiles(self):
        return self.__repo.getAllFiles()

    def add(self, title, element):
        """
        Simply checks if an element given as parameter is allowed to be set as a tag for the song, which referred by title, then it adds it if valid.
        """
        string = self.__repo.add(title, element)
        self.__stats = self.__repo.getAllStats()
        return string

    def replace(self, title, arguments):
        """deletes the arguments and replaces the space with new ones"""
        self.__repo.replace(title, arguments)
        self.__stats = self.__repo.getAllStats()

    def save(self):
        """
        Saves the information from the dictionary '__stats' into a file named with the version plus Heal.file.
        """
        self.__repo.save()

    def findByScore(self, items):
        """
        Calculates the score of the tags of each song, and returns a 2 dimensional list, first element is the song name, the second is the tags sum.
        """
        stuff = []
        i = 0
        for item in items:
            name, elements = item.split(":")
            score = 0
            #if name == "ï»¿test" or name == "": continue
            if "tag1" in elements: score += 10
            if "tag2" in elements: score += 2
            if "tag3" in elements: score += 6
            if "tag4" in elements: score += 5
            if "tag5" in elements: score += 4
            if "tag6" in elements: score += -3
            if "tag7" in elements: score += 7
            if "tag8" in elements: score += 6
            if "tag9" in elements: score += 7
            if "tag10" in elements: score += 2
            if "tag11" in elements: score += 4
            if "tag12" in elements: score += 7
            if "tag13" in elements: score += 6
            if "tag14" in elements: score += 12
            if "tag15" in elements: score += 6
            if "tag16" in elements: score += -7
            if "tag17" in elements: score += 1
            if "tag18" in elements: score += -12
            if "tag19" in elements: score += -15
            if "tag22" in elements: score += -100
            stuff.append([])
            stuff[i].append(name)
            stuff[i].append(score)
            i += 1
        return self.sorter(stuff)

    def sorter(self, stuff):
        """
        Sorts the songs by score.
        """
        stuff.sort(key=lambda x: x[1], reverse=True)
        return stuff

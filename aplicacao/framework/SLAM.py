class Slam():

    def __init__(self):
        self.bigger_key = None
        self.bigger_value = None
        self.landmark_dic = {}
    def biggerDictionaryKey(self, dictionary):
        """ gets bigger key in dictionary """
        #bigger value calculation
        self.bigger_value = max(dictionary.values())
        #bigger key calculation
        self.bigger_key = [key for key in dictionary.iterkeys() if 
                            dictionary[key] == self.bigger_value]
        self.bigger_key = self.bigger_key.pop()

        return self.bigger_key

    #abstractmethod
    def startAutomaticWalk():
        pass
        
    #abstractmethod
    def stopAutomaticWalk():
        pass
        
    def landmarkUpdate(self, key, value):
        self.landmark_dic[key] = value


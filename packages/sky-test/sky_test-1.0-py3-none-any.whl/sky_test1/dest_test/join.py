class club:
    def __init__(self,name):
        self.name=name
        self.people=[]
    def addpeople(self,peoplename):
        self.people.append(peoplename)
    def delpeople(self,peoplename):
        self.people.remove(peoplename)

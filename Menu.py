class Menu():
    menu = list()
    top = -1
    sub = -1
        
    def menuElement(self, name, content):
        subList = list()
        return {
                "Name"    : name,
                "Sub"     : subList,
                "Content" : content}
    
    def addTopElement(self, topEl):
        if not topEl in self.menu:
            self.menu.append(topEl)
    
    def addSubElement(self, topEl, subEl):
        if not subEl in topEl["Sub"]:
            topEl["Sub"].append(subEl)
            
    def nextTopElement(self):
        global top
        if len(self.menu) > 0:
            self.top +=1
            self.sub = -1
            if (self.top >= len(self.menu)):
                self.top = 0
        return self.menu[self.top]
    
    def prevTopElement(self):
        if len(self.menu) > 0:
            self.top -= 1
            self.sub = -1
            if (self.top < 0):
                self.top = len(self.menu)-1
        return self.menu[self.top]
    
    def nextSubElement(self):
        topEl = self.menu[self.top]
        if (len(topEl["Sub"]) > 0):
            self.sub += 1
            if (self.sub >= len(topEl["Sub"])):
                self.sub = 0
            return topEl["Sub"][self.sub]
        return self.menu[self.top]
    
    def prevSubElement(self):
        topEl = self.menu[self.top]
        if (len(topEl["Sub"]) > 0):
            self.sub -= 1
            if (self.sub == -1):
                return self.menu[self.top]
            if (self.sub < 0):
                print(self.sub)
                self.sub = len(topEl["Sub"])-1
                return topEl["Sub"][self.sub]
        return self.menu[self.top]
    

    
    def homeMenu(self):
        self.top = -1
        self.sub = -1
        return self.menu[0]
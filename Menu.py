#Daniel Juenger, github.com/sleeepyjack

import Adafruit_CharLCDPlate
from time import sleep
import commands
import psutil

class Menu():
    menu = list()
    top = 0
    sub = 0
    count = 1000
    element = None
    isInterrupted = False
    isOn = True
    isOnCount = 0
    stepScroll = 0
	
    def topElement(self, name, type, content):
        subList = list()
	sEl = self.subElement(name,type,content)
	subList.append(sEl)
        return {
                "Name"        : name,
                "Sub"         : subList,
		"Type"	      : type,
                "Content"     : content}

    def subElement(self, name, type, content):
        return {
                "Name"        : name,
		"Type"        : type,
                "Content"     : content}
	
    def buttonPressed(self, lcd):
        boo = False
        if (lcd.buttonPressed(lcd.SELECT) | lcd.buttonPressed(lcd.UP) | lcd.buttonPressed(lcd.DOWN) | lcd.buttonPressed(lcd.LEFT) | lcd.buttonPressed(lcd.RIGHT)):
            boo = True
        return boo

    def clearMenuRight(self, lcd):
        j = 0
        while(j < 16):
            lcd.scrollDisplayRight()
            sleep(.03)
            j += 1

    def clearMenuLeft(self, lcd):
        i = 0
        while(i < 16):
            lcd.scrollDisplayLeft()
            sleep(.03)
            i += 1

    def returnToTopElement(self):
        global element
	self.sub = 0
	self.element = self.menu[self.top]
		
    def firstTopElement(self):
	global element
        self.top = 0
        self.sub = 0
	self.element = self.menu[self.top]
        return self.element

    def addTopElement(self, topEl):
        if not topEl in self.menu:
            self.menu.append(topEl)

    def addSubElement(self, topEl, subEl):
        if not subEl in topEl["Sub"]:
            topEl["Sub"].append(subEl)

    def returnElement():
	global element
	return self.element

    def scroll(self, lcd, msg):
	global count
	global stepScroll
        if len(msg) > 16:
	    self.stepScroll = len(msg) - 16
	    if self.count <= 10 & self.stepScroll <= 0:
		lcd.scrollDisplayLeft()
		self.stepScroll -= 1
	    if self.count > 10:
		print "la"		
		    

    def nextTopElement(self, lcd):
	global element
	global count
	self.clearMenuLeft(lcd)
	self.count = 1000
        if len(self.menu) > 0:
            self.top = (self.top + 1) % len(self.menu)
            self.sub = 0
	    self.element = self.menu[self.top]
	self.handleMenu(lcd)

    def prevTopElement(self, lcd):
	global element
	global count
	self.clearMenuRight(lcd)
	self.count = 1000
        if len(self.menu) > 0:
            self.top -= 1
            self.sub  = 0
            if self.top < 0:
                self.top = len(self.menu)-1
	    self.element = self.menu[self.top]
	self.handleMenu(lcd)

    def nextSubElement(self, lcd):
	global element
	global count
        topEl = self.menu[self.top]
	self.count = 1000
        if (len(topEl["Sub"]) > 0):
            self.sub += 1
            if (self.sub >= len(topEl["Sub"])):
                self.sub = 0
            self.element = topEl["Sub"][self.sub]
	self.handleMenu(lcd)

    def prevSubElement(self, lcd):
	global element
	global count
        topEl = self.menu[self.top]
	self.count = 1000
        if (len(topEl["Sub"]) > 0):
            self.sub -= 1
            if (self.sub  < 0):
                self.sub = len(topEl["Sub"])-1
            self.element = topEl["Sub"][self.sub]
	self.handleMenu(lcd)

    def handleMenu(self,lcd):
	global element
	global count
	global isOn
	msg = ""
	if (self.count > 10) & self.isOn:
	    if self.element["Type"] == "STRING":
	        msg = self.element["Content"]
	    elif self.element["Type"] == "PYTHON":
		msg = str(eval(self.element["Content"]))
	    elif self.element["Type"] == "BASH":
	        msg = commands.getoutput(self.element["Content"])
	    self.count = 0
	    lcd.clear()
	    lcd.message(self.element["Name"]+"\n"+msg)
	    self.scroll(lcd, msg)
	self.count += 1

    def startMenu(self, lcd, color):
	global isInterrupted
	global isOn
	global isOnCount
	lcd.clear()
	lcd.backlight(color)
	selfisOnCount = 0
	self.firstTopElement()
	self.handleMenu(lcd)
	self.isOn = True
	self.isOnCount = 0
	self.isInterrupted = False
	while not self.isInterrupted:
	    try:
    		if self.isOn == True:
        		if lcd.buttonPressed(lcd.RIGHT):
                		self.nextTopElement(lcd)
                		self.isOnCount = 0
                		sleep(.3)
       			if lcd.buttonPressed(lcd.LEFT):
                		self.prevTopElement(lcd)
                		self.isOnCount = 0
                		sleep(.3)
        		if lcd.buttonPressed(lcd.DOWN):
                		self.nextSubElement(lcd)
                		self.isOnCount = 0
                		sleep(.3)
        		if lcd.buttonPressed(lcd.UP):
                		self.prevSubElement(lcd)
               			self.isOnCount = 0
                		sleep(.3)
			if lcd.buttonPressed(lcd.SELECT):
                		self.returnToTopElement()
               			self.isOnCount = 0
				print "s"
                		sleep(.3)
        		if self.isOnCount > 100:
                		lcd.backlight(lcd.OFF)
                		lcd.noDisplay()
                		self.isOnCount = 0
                		self.isOn = False
                		sleep(.3)

    		else:
       			if self.buttonPressed(lcd):
             	            lcd.display()
            		    lcd.backlight(color)
            		    self.isOnCount = 0
            		    self.isOn = True
           		    self.handleMenu(lcd)
            		    sleep(.3)
    		self.handleMenu(lcd)
    		sleep(.1)
    		self.isOnCount += 1
	    except KeyboardInterrupt:
		self.stopMenu(lcd)
    def stopMenu(self, lcd):
	global isInterrupted
	lcd.backlight(lcd.OFF)
	lcd.noDisplay()
	self.isInterrupted = True


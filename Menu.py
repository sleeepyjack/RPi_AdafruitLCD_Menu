# coding=utf-8
# Daniel Juenger, github.com/sleeepyjack
# updated to 3.x - James L. Key

import subprocess
from time import sleep
import Adafruit_CharLCD as Lcd


class Menu:
    menu = list()
    top = 0
    sub = 0
    count = 1000
    element = None
    isInterrupted = False
    isOn = True
    isOnCount = 0
    stepScroll = 0

    def top_element(self, name, element_type, content):
        """
        :param name: 
        :param element_type: 
        :param content: 
        :return List {Name: Sub: Element_type: Content}: 
        """
        sublist = list()
        subelement = self.sub_element(name, element_type, content)
        sublist.append(subelement)
        return {
            "Name": name,
            "Sub": sublist,
            "Type": element_type,
            "Content": content}

    @staticmethod
    def sub_element(name, element_type, content):
        """
        :param name: 
        :param element_type: 
        :param content: 
        :return: List {Name: Element_type: Content}: 
        """
        return {
            "Name": name,
            "Type": element_type,
            "Content": content}

    @staticmethod
    def button_pressed(lcd):
        """
        :param lcd: 
        :return:  Button Presses Boolean
        """
        boo = False
        if (lcd.is_pressed(Lcd.SELECT) | lcd.is_pressed(Lcd.UP) | lcd.is_pressed(Lcd.DOWN) | lcd.is_pressed(
                Lcd.LEFT) | lcd.is_pressed(Lcd.RIGHT)):
            boo = True
        return boo

    @staticmethod
    def clear_menu_right(lcd):
        """
        :param lcd: 
        """
        j = 0
        while j < 16:
            lcd.move_right()
            sleep(.03)
            j += 1

    @staticmethod
    def clear_menu_left(lcd):
        """
        :param lcd: 
        """
        i = 0
        while i < 16:
            lcd.move_left()
            sleep(.03)
            i += 1

    def return_to_top_element(self):
        global element
        self.sub = 0
        self.element = self.menu[self.top]

    def first_top_element(self):
        """
        :return: Element 
        """
        global element
        self.top = 0
        self.sub = 0
        self.element = self.menu[self.top]
        return self.element

    def add_top_element(self, top_element):
        """
        :param top_element: 
        """
        if top_element not in self.menu:
            self.menu.append(top_element)

    @staticmethod
    def add_sub_element(top_element, sub_element):
        """
        :param top_element: 
        :param sub_element: 
        """
        if sub_element not in top_element["Sub"]:
            top_element["Sub"].append(sub_element)

    def return_element(self):
        """
        :return: Element
        """
        global element
        return self.element

    def scroll(self, lcd, msg):
        """
        :param lcd: 
        :param msg: 
        """
        global count
        global stepScroll
        if len(msg) > 16:
            self.stepScroll = len(msg) - 16
            if self.count <= 10 & self.stepScroll <= 0:
                lcd.scrollDisplayLeft()
                self.stepScroll -= 1
            if self.count > 10:
                print("la")

    def next_top_element(self, lcd):
        """
        :param lcd: 
        """
        global element
        global count
        self.clear_menu_left(lcd)
        self.count = 1000
        if len(self.menu) > 0:
            self.top = (self.top + 1) % len(self.menu)
            self.sub = 0
            self.element = self.menu[self.top]
        self.handle_menu(lcd)

    def prev_top_element(self, lcd):
        """
        :param lcd: 
        """
        global element
        global count
        self.clear_menu_right(lcd)
        self.count = 1000
        if len(self.menu) > 0:
            self.top -= 1
            self.sub = 0
            if self.top < 0:
                self.top = len(self.menu) - 1
            self.element = self.menu[self.top]
        self.handle_menu(lcd)

    def next_sub_element(self, lcd):
        """
        :param lcd: 
        """
        global element
        global count
        top_el = self.menu[self.top]
        self.count = 1000
        if len(top_el["Sub"]) > 0:
            self.sub += 1
            if self.sub >= len(top_el["Sub"]):
                self.sub = 0
            self.element = top_el["Sub"][self.sub]
        self.handle_menu(lcd)

    def prev_sub_element(self, lcd):
        """
        :param lcd: 
        """
        global element
        global count
        top_el = self.menu[self.top]
        self.count = 1000
        if len(top_el["Sub"]) > 0:
            self.sub -= 1
            if self.sub < 0:
                self.sub = len(top_el["Sub"]) - 1
            self.element = top_el["Sub"][self.sub]
        self.handle_menu(lcd)

    def handle_menu(self, lcd):
        """
        :param lcd: 
        """
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
                msg = subprocess.getoutput(self.element["Content"])
            self.count = 0
            lcd.clear()
            lcd.message(self.element["Name"] + "\n" + msg)
            self.scroll(lcd, msg)
        self.count += 1

    def start_menu(self, lcd):
        """
        :param lcd: 
        """
        global isInterrupted
        global isOn
        global isOnCount
        lcd.clear()
        lcd.set_color(0, 1, 1)
        self.isOnCount = 0
        self.first_top_element()
        self.handle_menu(lcd)
        self.isOn = True
        self.isOnCount = 0
        self.isInterrupted = False
        while not self.isInterrupted:
            try:
                if self.isOn:
                    if lcd.is_pressed(Lcd.RIGHT):
                        self.next_top_element(lcd)
                        self.isOnCount = 0
                        sleep(.3)
                    if lcd.is_pressed(Lcd.LEFT):
                        self.prev_top_element(lcd)
                        self.isOnCount = 0
                        sleep(.3)
                    if lcd.is_pressed(Lcd.DOWN):
                        self.next_sub_element(lcd)
                        self.isOnCount = 0
                        sleep(.3)
                    if lcd.is_pressed(Lcd.UP):
                        self.prev_sub_element(lcd)
                        self.isOnCount = 0
                        sleep(.3)
                    if lcd.is_pressed(Lcd.SELECT):
                        self.return_to_top_element()
                        self.isOnCount = 0
                        print("s")
                        sleep(.3)
                    if self.isOnCount > 100:
                        lcd.set_backlight(0.0)
                        lcd.enable_display(False)
                        self.isOnCount = 0
                        self.isOn = False
                        sleep(.3)

                else:
                    if self.button_pressed(lcd):
                        lcd.enable_display(True)
                        lcd.set_color(0, 1, 1)
                        self.isOnCount = 0
                        self.isOn = True
                        self.handle_menu(lcd)
                        sleep(.3)
                self.handle_menu(lcd)
                sleep(.1)
                self.isOnCount += 1
            except KeyboardInterrupt:
                self.stop_menu(lcd)

    def stop_menu(self, lcd):
        """
        :param lcd: 
        """
        global isInterrupted
        lcd.set_backlight(0.0)
        lcd.enable_display(False)
        self.isInterrupted = True

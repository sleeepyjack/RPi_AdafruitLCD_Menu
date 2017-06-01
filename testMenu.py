# coding=utf-8
# Daniel Juenger, github.com/sleeepyjack
# updated to 3.x - James L. Key

from time import sleep
import Adafruit_CharLCD as Lcd
from Menu import Menu

lcd = Lcd.Adafruit_CharLCDPlate()
menu = Menu()

# The menu can show strings, bash and python expressions

# --------- top_element(      Name , Type of content , Lower row content)

top1 = menu.top_element("< Network      >", "STRING", "        v")
top2 = menu.top_element("< System       >", "STRING", "        v")
top3 = menu.top_element("< top3         >", "STRING", "        v")
top4 = menu.top_element("< top4         >", "STRING", "        v")
top5 = menu.top_element("< top5         >", "STRING", "        v")
sub11 = menu.sub_element("Net.>Signal", "BASH",
                         "iwconfig wlan0 | awk -F'[ =]+' '/Signal level/ {print $7}' | cut -d/ -f1")
sub12 = menu.sub_element("Net.>SSID", "BASH",
                         "iwconfig wlan0 | grep 'ESSID:' | awk '{print $4}' | sed 's/ESSID://g'")
sub13 = menu.sub_element("Net.>Internet", "BASH",
                         "ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error")
sub21 = menu.sub_element("System>CPU", "PYTHON3",
                         'str(str(psutil.cpu_percent()) + "%")')
sub22 = menu.sub_element("System>CPU-Temp.", "STRING", "TODO")
sub23 = menu.sub_element("System>RAM", "PYTHON3",
                         'str(str(psutil.virtual_memory()[2])+"% used")')

# Adding elements to the menu
menu.add_top_element(top1)
menu.add_top_element(top2)
menu.add_top_element(top3)
menu.add_top_element(top4)
menu.add_top_element(top5)

menu.add_sub_element(top1, sub11)
menu.add_sub_element(top1, sub12)
menu.add_sub_element(top1, sub13)
menu.add_sub_element(top2, sub21)
menu.add_sub_element(top2, sub22)
menu.add_sub_element(top2, sub23)


# initializing display
lcd.clear()
lcd.set_color(0, 1, 1)

# little loading animation
i = 0
lcd.message("LOADING\n")
while i < 16:
    lcd.message(chr(219))
    sleep(.1)
    i += 1

# starting the menu
menu.start_menu(lcd)

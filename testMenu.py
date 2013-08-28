#Daniel Juenger, github.com/sleeepyjack

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from menu import Menu

lcd = Adafruit_CharLCDPlate()
menu = Menu()

#The menu can show strings, bash and python expressions

#		     topElement(      Name , Type of content , Lower row content)

top1 = menu.topElement("< Netzwerk     >", "STRING", "        v")
top2 = menu.topElement("< System       >", "STRING", "        v")
top3 = menu.topElement("< top3         >", "STRING", "        v")
top4 = menu.topElement("< top4         >", "STRING", "        v")
top5 = menu.topElement("< top5         >", "STRING", "        v")
sub11 = menu.subElement("Netzw.>Signal", "BASH", "iwconfig wlan0 | awk -F'[ =]+' '/Signal level/ {print $7}' | cut -d/ -f1")
sub12 = menu.subElement("Netzw.>SSID", "BASH", "iwconfig wlan0 | grep 'ESSID:' | awk '{print $4}' | sed 's/ESSID://g'")
sub13 = menu.subElement("Netzw.>Internet", "BASH", "ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error")
sub21 = menu.subElement("System>CPU", "PYTHON", 'str(str(psutil.cpu_percent()) + "%")')
sub22 = menu.subElement("System>CPU-Temp.", "STRING", "TODO")
sub23 = menu.subElement("System>RAM", "PYTHON", 'str(str(psutil.phymem_usage()[3])+"% used")')

#Adding elements to the menu
menu.addTopElement(top1)
menu.addTopElement(top2)
menu.addTopElement(top3)
menu.addTopElement(top4)
menu.addTopElement(top5)

menu.addSubElement(top1, sub11)
menu.addSubElement(top1, sub12)
menu.addSubElement(top1, sub13)
menu.addSubElement(top2, sub21)
menu.addSubElement(top2, sub22)
menu.addSubElement(top2, sub23)

color = lcd.TEAL

#initializing display
lcd.clear()
lcd.backlight(color)

#little loading animation
i = 0
lcd.message("LOADING\n")
while(i < 16):
    lcd.message(chr(219))
    sleep(.1)
    i += 1

#starting the menu
menu.startMenu(lcd, color)


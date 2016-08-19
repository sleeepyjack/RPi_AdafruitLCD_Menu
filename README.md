RPi_AdafruitLCD_Menu
====================

Demo video: http://www.youtube.com/watch?v=d60a9SgJH-w

Two dimensional menu for the Adafruit RGB LCD Plate (see: http://www.adafruit.com/products/1110) on Raspberry Pi



The menu contains top elements wich can be cycled through horizontally.
Every top element can contain sub elements wich can be cycled through vertically.

The content of every element can be either a string, a bash or python expression, wich will be updated about every second.
For example you can show the cpu or network stats of your RPi.

The display will automatically turn off after some seconds and, what's also nice, will stop the updating process of the current menu element to show.
It will turn back on and show the last shown element when any button is clicked.

To use this menu you will have to download the Adafruit library for the LCD:
UPDATED to support current Adafruit LCD libraries (see: https://github.com/adafruit/Adafruit_Python_CharLCD)


For further understanding look into the testMenu.py or contact me.

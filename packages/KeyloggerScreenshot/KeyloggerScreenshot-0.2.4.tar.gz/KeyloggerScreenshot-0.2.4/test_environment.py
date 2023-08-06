import PIL.Image
import pyautogui as pg
import random
import time

for x in range(1):
    num = x +1
    img = PIL.Image.open(f"New_Image ({num}).png")
    img.show()
    pg.press("f11")
    pg.moveTo(random.randint(100, 800), random.randint(100, 800), 0.3)
    pg.press("esc")
    pg.sleep(3)
"""Final stage of process, YEAH!"""
import os
import ctypes
from PIL import Image


def get_set_wallpaper(width, height):
    """It just does what it is suppose to do"""
    PATH = os.getcwd()
    wallp = Image.open(PATH+'\\wallpaper.jpg')

    PATH += '\\assets'
    rozv = Image.open(PATH+'\\page.png')

    imgmap = wallp.load()
    wpw, wph = wallp.size
    # row, roh = rozv.size
    row, roh = width, height

    # stupidly done, but hey, if it works...
    x0_ = wpw - row - 20
    y0_ = wph - roh - 92

    for x in range(width):
        for y in range(height):
            imgmap[x0_+x, y0_+y] = rozv.getpixel((x+10, y+10))

    wallp.save(PATH+"\\final.png")

    # set wallpaper
    SPI_SETDESKWALLPAPER = 20

    PATH += '\\final.png'
    # print('set wp: ', PATH)

    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, PATH, 3)

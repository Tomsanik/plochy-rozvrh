"""Final stage of the process, YEAH!"""
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
    row, roh = rozv.size

    # stupidly done, but hey, if it works...
    x0_ = wpw - row - 20
    y0_ = wph - roh - 92

    for x__ in range(width):
        for __ in range(height):
            imgmap[x0_+x__, y0_+__] = rozv.getpixel((x__+10, __+10))

    wallp.save(PATH+"\\final.png")

    # set wallpaper
    SPI_SETDESKWALLPAPER = 20

    PATH += '\\final.png'
    # print('set wp: ', PATH)

    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, PATH, 3)

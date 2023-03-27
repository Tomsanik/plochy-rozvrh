"""Final stage of process, YEAH!"""
import os
import ctypes
from PIL import Image


def get_set_wallpaper(width, height):
    """It just does what it is supposed to do"""
    PATH = os.getcwd()
    wallp = Image.open(PATH+'\\wallpaper2.jpg')

    PATH += '\\assets'
    rozv = Image.open(PATH+'\\page.png')

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    imgmap = wallp.load()
    scw, swh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    wpw, wph = wallp.size
    k = wpw/scw
    new_size = (int(rozv.size[0] * k), int(rozv.size[1] * k))
    rozv = rozv.resize(new_size)

    row, roh = int(width*k), int(height*k-6)

    # stupidly done, but hey, if it works...
    x0w = wpw - row - int(20*k)
    y0w = wph - roh - int(92*k)
    x0r, y0r = int(10*k), int(10*k)

    for x in range(row):
        for y in range(roh):
            imgmap[x0w+x, y0w+y] = rozv.getpixel((x0r+x, y0r+y))

    wallp.save(PATH+"\\final.png")

    # set wallpaper
    SPI_SETDESKWALLPAPER = 20

    PATH += '\\final.png'
    # print('set wp: ', PATH)

    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, PATH, 3)

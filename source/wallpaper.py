from PIL import Image
import ctypes
import os


def get_set_wallpaper(w, h):
    PATH = os.getcwd()
    wp = Image.open(PATH+'\\wallpaper.jpg')

    PATH += '\\assets'
    rz = Image.open(PATH+'\\page.png')

    imgmap = wp.load()
    ww, wh = wp.size
    rw, rh = rz.size

    # stupidly done, but hey, if works...
    x0 = ww - rw - 20
    y0 = wh - rh - 92

    # print(rw, rh)
    # print(x0, y0)
    # print(ww, wh)
    for x in range(w):
        for y in range(h):
            imgmap[x0+x, y0+y] = rz.getpixel((x+10, y+10))

    wp.save(PATH+"\\final.png")

    # set wallpaper
    SPI_SETDESKWALLPAPER = 20
    
    PATH += '\\final.png'
    # print('set wp: ', PATH)
    
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, PATH, 3)

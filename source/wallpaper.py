"""Final stage of process, YEAH!"""
import os
import ctypes
from PIL import Image
from html2image import Html2Image
import time


def get_set_wallpaper(width, height, size):
    """It just does what it is supposed to do"""
    PATH = os.getcwd()
    wallp = Image.open(os.path.join(PATH, 'wallpaper.jpg'))
    wpw, wph = wallp.size

    # create image from html
    zoom = round(wpw*size/width, 2)
    width = round(zoom*width)
    height = round(zoom * (height-5))
    with open(os.path.join(PATH, 'assets', 'rozvrh.html'), encoding='utf-8') as f:
        html = f.read()
    html = html.format(now=time.strftime("%H:%M:%S", time.localtime()), zoom=zoom)

    hti = Html2Image(output_path=os.path.join(PATH, 'assets'))

    x0r, y0r = round(8 * zoom), round(8 * zoom)
    screenshot_size = (width + x0r, height + y0r)

    hti.screenshot(html_str=html,
                   css_file=os.path.join(PATH, 'source', 'rozvrh.css'),
                   save_as='page.png',
                   size=screenshot_size)
    # print(f"Screenshot saved to {os.path.join(output_dir, 'page.png')}")

    PATH += '\\assets'
    rozv = Image.open(PATH+'\\page.png')
    imgmap = wallp.load()

    x0w = wpw*0.99 - width
    y0w = wph*0.95 - height
    for x in range(width):
        for y in range(height):
            imgmap[x0w+x, y0w+y] = rozv.getpixel((x+x0r, y+y0r))

    wallp.save(PATH+"\\final.png")

    # set wallpaper
    SPI_SETDESKWALLPAPER = 20

    PATH += '\\final.png'
    # print('set wp: ', PATH)

    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, PATH, 3)

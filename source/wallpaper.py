"""Final stage of process, YEAH!"""
import ctypes
import os
import time

from PIL import Image
from html2image import Html2Image


# def get_set_wallpaper_new(width, height, size):
#     user32 = ctypes.windll.user32
#     user32.SetProcessDPIAware()
#     # screen size
#     sw, sh = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
#
#     PATH = os.getcwd()
#     wallp = Image.open(os.path.join(PATH, 'wallpaper.jpg'))
#     ww, wh = wallp.size
#     img = wallp.load()
#
#     print(sw, sh, ww, wh)
#
#     if sw > sh:
#         i = int(sw-ww)/2

def get_set_wallpaper_old(width, height, size):
    """It just does what it is supposed to do"""
    user32 = ctypes.windll.user32
    sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    PATH = os.getcwd()
    wallp = Image.open(os.path.join(PATH, 'wallpaper.jpg'))
    wpw, wph = wallp.size

    # create image from html
    zoom = round(wpw * size / width, 2)  # size = fraction of wallpaper width taken by timetable
    print(wpw, size, width, zoom)
    width = round(zoom * width)
    height = round(zoom * (height - 5))
    with open(os.path.join(PATH, 'assets', 'rozvrh.html'), encoding='utf-8') as f:
        html = f.read()
    html = html.format(now=time.strftime("%H:%M:%S", time.localtime()), zoom=zoom)

    x0r, y0r = round(8 * zoom*1.25), round(8 * zoom*1.25)
    width = round(width*1.25)
    height = round(height*1.25)
    screenshot_size = (width + x0r, height + y0r)
    hti = Html2Image(output_path=os.path.join(PATH, 'assets'))
    hti.size = screenshot_size

    print(screenshot_size)
    hti.browser.use_new_headless = None
    hti.screenshot(html_str=html,
                   css_file=os.path.join(PATH, 'source', 'rozvrh.css'),
                   save_as='page.png')
    # print(f"Screenshot saved to {os.path.join(output_dir, 'page.png')}")

    PATH += '\\assets'
    rozv = Image.open(PATH + '\\page.png')
    # rr = rozv.load()
    # for x in range(20):
    #     for y in range(20):
    #         if rr[x, y] != (0, 0, 0, 0):
    #             x0r, y0r = x, y
    imgmap = wallp.load()

    x0w = wpw * 0.99 - width
    y0w = wph * 0.95 - height
    for x in range(width):
        for y in range(height):
            imgmap[x0w + x, y0w + y] = rozv.getpixel((x + x0r, y + y0r))

    wallp.save(PATH + "\\final.png")

    # set wallpaper
    SPI_SETDESKWALLPAPER = 20

    PATH += '\\final.png'
    # print('set wp: ', PATH)

    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, PATH, 3)


def get_set_wallpaper(width, height, size):
    """It just does (not do) what it is supposed to do"""
    BACK_COLOR = 'ACACAC'
    PATH = os.getcwd()
    wallp = Image.open(os.path.join(PATH, 'wallpaper.jpg'))
    wpw, wph = wallp.size

    user32 = ctypes.windll.user32
    sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    sc_x0 = 0
    if wpw / wph > sw / sh:
        wpw2 = sw / sh * wph
        sc_x0 = (wpw - wpw2)/2
        wpw = wpw2

    # create image from html
    zoom = round(wpw * size / width, 2)  # size = fraction of wallpaper width taken by timetable
    # print(wpw, size, width, zoom)
    # print((width, height))

    with open(os.path.join(PATH, 'assets', 'rozvrh.html'), encoding='utf-8') as f:
        html = f.read()
    html = html.format(now=time.strftime("%H:%M:%S", time.localtime()), zoom=zoom)

    hti = Html2Image(custom_flags=['--default-background-color='+BACK_COLOR, '--hide-scrollbars'],
                     output_path=os.path.join(PATH, 'assets'))
    hti.browser.use_new_headless = None
    # hti.browser.print_command = True
    hti.screenshot(html_str=html,
                   css_file=os.path.join(PATH, 'source', 'rozvrh.css'),
                   save_as='page.png')
    print(f"Screenshot saved to {'./page.png'}")

    PATH += '\\assets'
    rozv = Image.open(PATH + '\\page.png')

    imgmap = wallp.load()
    width = round(zoom * width)
    height = round(zoom * height)
    x0w = wpw * 0.99 - width+sc_x0
    y0w = wph * 0.92 - height
    back_color = tuple(int(BACK_COLOR[i:i + 2], 16) for i in (0, 2, 4))
    for x in range(width+20):
        for y in range(height+20):
            pxl = rozv.getpixel((x, y))
            if pxl != back_color:
                imgmap[x0w + x, y0w + y] = pxl

    wallp.save(PATH + "\\final.png")

    PATH += '\\final.png'
    ctypes.windll.user32.SystemParametersInfoW(20, 0, PATH, 3)


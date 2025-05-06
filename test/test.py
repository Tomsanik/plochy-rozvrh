import ctypes
import os
import time
from PIL import Image
from html2image import Html2Image


def get_set_wallpaper(width, height, size):
    # print(os.getcwd())
    user32 = ctypes.windll.user32
    screen_dpiw = user32.GetSystemMetrics(0)
    user32.SetProcessDPIAware()
    screen_realw = user32.GetSystemMetrics(0)
    dpi = screen_realw / screen_dpiw
    # print('scrn res: ', screen_realw, screen_dpiw, f'k={dpi_sett}')

    """It just does (not do) what it is supposed to do"""
    PATH = os.getcwd()
    wallp = Image.open(os.path.join(PATH, '../wallpaper.jpg'))
    wpw, wph = wallp.size

    # create image from html
    zoom = round(wpw * size / width, 2)  # size = fraction of wallpaper width taken by timetable
    print(wpw, size, width, zoom)
    width = round(zoom * width)
    height = round(zoom * height)

    # x0r, y0r = round(8 * zoom), round(8 * zoom)
    x0r, y0r = 50, 110
    # width = round(width)
    # height = round(height)
    screenshot_size = ((width + x0r)/dpi, (height + y0r)/dpi)
    print(screenshot_size)
    # print(wpw*size)

    with open('rozvrh.html', encoding='utf-8') as f:
        html = f.read()
    html = html.format(now=time.strftime("%H:%M:%S", time.localtime()), zoom=1)

    hti = Html2Image(size=screenshot_size, custom_flags=['--default-background-color=FF0000', '--hide-scrollbars'])
    hti.browser.use_new_headless = None
    hti.browser.print_command = True
    hti.screenshot(html_str=html,
                   css_file='rozvrh.css',
                   save_as='page.png')
    print(f"Screenshot saved to {'./page.png'}")

    # PATH += '\\assets'
    # rozv = Image.open(PATH + '\\page.png')
    # # rr = rozv.load()
    # # for x in range(20):
    # #     for y in range(20):
    # #         if rr[x, y] != (0, 0, 0, 0):
    # #             x0r, y0r = x, y
    # imgmap = wallp.load()
    #
    # x0w = wpw * 0.99 - width
    # y0w = wph * 0.95 - height
    # for x in range(width):
    #     for y in range(height):
    #         imgmap[x0w + x, y0w + y] = rozv.getpixel((x + x0r, y + y0r))
    #
    # wallp.save(PATH + "\\final.png")


get_set_wallpaper(500, 359, 0.5)

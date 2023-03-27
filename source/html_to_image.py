"""HTMLs to IMG"""
import os
from html2image import Html2Image


def html_img(width, height):
    """Needs Chrome to be installed"""
    PATH = os.getcwd()
    output_dir = os.path.join(PATH, 'assets')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    hti = Html2Image(output_path=output_dir)
    screenshot_size = (width+10, height+10)
    print(screenshot_size)
    hti.screenshot(html_file=os.path.join(PATH, 'assets', 'rozvrh.html'),
                   css_file=os.path.join(PATH, 'source', 'rozvrh.css'),
                   save_as='page.png',
                   size=screenshot_size)
    print(f"Screenshot saved to {os.path.join(output_dir, 'page.png')}")


def html_img2(width, height):
    """Needs Chrome to be installed"""
    PATH = os.getcwd()
    # print(PATH+'\\assets\\rozvrh.html')
    hti = Html2Image(output_path=PATH + '\\assets')  #, custom_flags=['--no-sandbox'])
    # print(hti.output_path)
    # print(width, height)

    width += 10
    height += 10
    hti.screenshot(html_file=PATH + '\\assets\\rozvrh.html', css_file=PATH + '\\source\\rozvrh.css', save_as='page.png',
                   size=(width, height))

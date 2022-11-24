"""HTMLs to IMG"""
import os
from html2image import Html2Image


def html_img(width, height):
    """Needs Chrome to be installed"""
    PATH = os.getcwd()
    hti = Html2Image(output_path=PATH+'\\assets')

    width += 10
    height += 10
    hti.screenshot(html_file=PATH+'\\assets\\rozvrh.html', css_file=PATH +
                   '\\source\\rozvrh.css', save_as='page.png', size=(width, height))

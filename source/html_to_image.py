from html2image import Html2Image
import os


def html_img(w, h):
    # needs Chrome
    PATH = os.getcwd()
    hti = Html2Image(output_path=PATH+'\\assets')

    w += 10
    h += 10
    hti.screenshot(html_file=PATH+'\\assets\\rozvrh.html', css_file=PATH+'\\source\\rozvrh.css', save_as='page.png', size=(w, h))

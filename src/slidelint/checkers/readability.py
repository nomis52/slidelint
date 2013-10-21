from slidelint.utils import help
import os
import tempdir
import subprocess
from lxml import html
from slidelint.pdf_utils import document_pages_layouts, layout_characters
from PIL import Image, ImageDraw
import re
from math import exp

messages = (
    dict(id='C3000',
         msg_name='text-readability',
         msg='Text is not readable enough',
         help="Change text or background color"),)


def tranform2html(source, dist, out_name='out.html'):
    outpath = os.path.join(dist, out_name)
    cmd = ['pdftohtml', '-c', '-noframes', '-zoom', '1',
           source, outpath]
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,)
    process.wait()
    files = os.listdir(dist)
    files.sort()
    files.pop(files.index(out_name))
    html = open(outpath, 'rb').read()
    return html, [os.path.join(dist, f) for f in files]


class TextColorExtractor():
    def __init__(self, raw_html):
        root = html.fromstring(raw_html)
        body = root.find('body')
        styles = [re.findall('\.(ft\w+)\{.*color:#([\w|\d]+).*\}', i.text)
                  for i in body.findall("style")]
        self.class_color_mapping = dict(sum(styles, []))
        self.pages = [page for page in body.findall('div')]

    def __call__(self, page_num):
        page = self.pages[page_num]
        for paragraph in page.findall('p'):
            color = self.class_color_mapping[paragraph.get('class', 'ft00')]
            for character in "".join(paragraph.itertext()):
                if character not in (u'\xa0',) and ord(character ) > 32:
                    yield color, character


def get_text_color_and_background(color_extractor, page_layout,
                                  page_background, page_num):
    for character, color in zip(layout_characters(page_layout), color_extractor(page_num)):
        if character._text != color[1]:
            raise ValueError("Characters mismatch: '%s' != '%s'", character, color)
        x0, y0, x1, y1 = map(int, character.bbox)
        box = (x0, page_layout.height - y1, x1, page_layout.height - y0)
        character_background = page_background.crop(box)
        yield color[1], color[0], character_background


def goes_throught_pages(source):
    with tempdir.TempDir() as dist:
        html, images = tranform2html(source, dist)
        color_extractor = TextColorExtractor(html)
        document_layout = document_pages_layouts(source)
        for (page_num, page_layout), image_path in zip(document_layout, images):
            page_background = Image.open(image_path)
            page_images = get_text_color_and_background(
                color_extractor, page_layout, page_background, page_num)
            yield page_num, page_images


def html_color_to_grayscale(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    grayscale = r * 299/1000 + g * 587/1000 + g * 114/1000
    return int(grayscale)


class VisibilityChecker():
    def __init__(self, scale, s_range=50):
        self.scale = scale
        self.range = s_range
        self.cc = [exp(i/10.0) for i in range(1, self.range+1)]

    def colors_slice_sum(self, colors_slice):
        return sum([d / k for k, d in zip(self.cc, colors_slice)])

    def __call__(self, html_color, background):
        histogram = background.convert('L').histogram()
        grayscale_color = html_color_to_grayscale(html_color)
        start = grayscale_color - self.range
        end = grayscale_color + self.range
        total_colors = sum(histogram)
        left_colors_slice = histogram[start if start > 0 else 0:grayscale_color]
        right_colors_slice = histogram[grayscale_color + 1:end if end < 256 else None]
        main_color = histogram[grayscale_color]
        veight = main_color + sum(map(self.colors_slice_sum, (left_colors_slice[::-1], right_colors_slice)))
        similarity = veight / total_colors
        return similarity


def main(target_file=None, msg_info=None):
    if msg_info:
        return help(messages, msg_info)
    scale = 1
    max_similarity = 0.1
    rez = []
    visibility_checker = VisibilityChecker(scale)
    for page_num, page_data in goes_throught_pages(target_file):
        for character, character_color, background in page_data:
            similarity = visibility_checker(character_color, background)
            if similarity > max_similarity:
                rez.append(dict(id='C3000',
                                msg_name='text-readability',
                                msg='Text is not readable enough %s' % character,
                                help="Change text or background color",
                                page='%s' % (page_num + 1)))
                break
    return rez

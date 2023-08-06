import time
from datetime import datetime

import minify_html.minify_html
from bs4 import BeautifulSoup


def user_agent():
    return {"User-Agent": "https://github.com/ksh-b/eintf"}


def convert_time(orig_date, orig_format):
    # IDK why but timestamps are off by a day
    return int(datetime.strptime(orig_date, orig_format).timestamp()) + 86400


def cleanse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all():
        if tag.name != "a" and tag.name != "img":
            tag.attrs = {}
    return minify_html.minify(str(soup), minify_js=True, minify_css=True, remove_processing_instructions=True)


def now():
    return int(time.time())

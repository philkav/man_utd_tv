#!/usr/bin/python
# -*- coding: utf-8 -*-
# Philip Kavanagh (https://github.com/philkav)
import requests
from bs4 import BeautifulSoup
import json


def extract_fluid_rows(html_text):
        fix_list = []
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find_all("div", {"class": "row-fluid"})


def rip_class(text, resset):
        line = resset.find("div", {"class": text})
        if line is not None:
            return line.text.encode('utf-8')


def arrange(frows):
    matches = []
    current_date = ""
    current_match = ""
    for f in frows:
        date = rip_class("span12 matchdate", f)
        match = rip_class("span4 matchfixture", f)
        comp = rip_class("span4 competition", f)
        time = rip_class("span1 kickofftime", f)
        channels = rip_class("span3 channels", f)

        if date is not None: current_date = date
        if match is None: continue
        matches.append({ "date" : current_date, "fixture" : match, "comp" : comp, "time" : time, "channels" : channels })

    return matches


def get_fixtures(url):
    r = requests.get(url)
    if r.status_code != 200: return []

    fluid_rows = extract_fluid_rows(r.text)
    return arrange(fluid_rows)


def table_view(text):
    print "{:<30}|{:<48}|{:<48}|{:<20}|{:<40}".format(
            text['date'], text['fixture'], text['comp'], text['time'], text['channels'])


if __name__ == '__main__':
    url = "https://www.live-footballontv.com/"
    for f in get_fixtures(url):
        if "Man Utd" in f['fixture']: table_view(f)

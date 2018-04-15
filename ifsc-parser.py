#!/usr/bin/env python3

""" IFSC Event to icalendar parser.

    This program fetches the events from the IFSC bouldering worldcup
    and converts them to an ical file which can be read by e.g. Thunderbird.
    The output will be written to 'cal_olypark.ics' in the current directory.
    One may wants to adjust the 'url_*' variables below.
"""

# -*- coding: utf-8 -*-

import os
import icalendar as ical
import urllib.request
import dateutil.parser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

url_wc = 'https://www.ifsc-climbing.org/index.php/component/ifsc/?year={}&filter=world_cups'.format(datetime.now().year)
url_champ = 'https://www.ifsc-climbing.org/index.php/component/ifsc/?year={}&filter=championships'.format(datetime.now().year)

competitions = []
for url in [url_wc, url_champ]:
    raw_html = urllib.request.urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(raw_html, 'html.parser')
    competitions += soup.find_all("div", class_="competition")

events = []
for comp in competitions:
    title = comp.find("div", class_="title").getText(strip=True)
    date = comp.find("div", class_="date").getText(strip=True)
    events.append({'date': date, 'title': title})


def split_date(ev):
    split = ev.split("-")
    start = split[0].strip()
    end = split[1].strip()
    end_date = dateutil.parser.parse(end)
    start_date = end_date.replace(day=int(start))

    return {"start_date": start_date, "end_date": end_date}


cal = ical.Calendar()
for ev in events:
    splitd = split_date(ev['date'])

    ical_ev = ical.Event()

    ical_ev.add('summary', ev['title'])
    ical_ev.add('dtstart', splitd['start_date'].date())
    ical_ev.add('dtend', splitd['end_date'].date() + timedelta(days=1))

    cal.add_component(ical_ev)


directory = os.path.dirname(os.path.realpath('__file__'))
f = open(os.path.join(directory, 'ifsc_cal.ics'), 'wb')
f.write(cal.to_ical())
f.close()

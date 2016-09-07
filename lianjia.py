#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')


def run(q):
    import requests
    from BeautifulSoup import BeautifulSoup as Soup
    from soupselect import select
    from alfred.feedback import Feedback

    fb = Feedback()

    q = q.strip()
    url = 'http://bj.lianjia.com/chengjiao/rs%s' % q
    r = requests.get(url)
    r.encoding = 'utf8'
    content = r.text
    soup = Soup(content)
    items = select(soup, 'ul.listContent li')
    for item in items:
        try:
            deal_date = select(item, 'div.dealDate')[0].text
            title = select(item, 'div.title a')[0].text
            price = select(item, 'div.totalPrice')[0].text
            unit_price = select(item, 'div.unitPrice')[0].text
            link = select(item, 'div.title a')[0]['href']
            kwargs = {
                'title': title,
                'subtitle': deal_date + '成交' + ' ' + price + ' ' + unit_price,
                'arg': link,
            }
            fb.addItem(**kwargs)
        except:
            pass

    fb.output()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit()
    query = sys.argv[1]
    run(query)

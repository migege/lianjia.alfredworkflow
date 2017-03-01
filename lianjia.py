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
    url = 'http://m.lianjia.com/bj/chengjiao/rs%s' % q
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Referer': 'https://m.lianjia.com/bj/sold/search/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    r = requests.get(url, headers=headers)
    r.encoding = 'utf8'
    content = r.text
    soup = Soup(content)
    items = select(soup, 'ul.lists li.pictext')
    for item in items:
        try:
            deal_date = select(item, 'div.item_date')[0].text
            title = select(item, 'div.item_main')[0].text
            desc = select(item, 'span.q_oriention')[0].text
            price = select(item, 'span.price_total')[0].text
            unit_price = select(item, 'span.unit_price')[0].text
            link = select(item, 'a.flexbox')[0]['href']
            kwargs = {
                'title': title + ' ' + price + ' ' + unit_price,
                'subtitle': deal_date + '成交' + ' ' + '位置：' + desc,
                'arg': 'https://m.lianjia.com' + link,
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

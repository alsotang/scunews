# coding=utf-8

import webapp2
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
# from google.appengine.ext import deferred

import re, htmlentitydefs
import json
import urlparse
import logging

from model import PageContent
import fix_path
from fetch_config import config as fetch_config

from BeautifulSoup import BeautifulSoup as bs

# if os.environ['SERVER_NAME'] == 'localhost':
#     logging.info('set debug level to debug')
#     logging.getLogger().setLevel(logging.DEBUG)

class FetchHandler(webapp2.RequestHandler):
    def get(self):
        for site_id, site_attrs in fetch_config.iteritems():
            taskqueue.add(url='/start_fetch', params={'url':site_attrs['url'], 'site_id': site_id, 'is_index': True})

        self.response.write('start fetching...')
    def post(self):
        url, site_id, is_index = self.request.get('url'), self.request.get('site_id'), self.request.get('is_index')
        logging.info('fetching...%s' % url)
        defer_fetch(url, site_id, is_index)


def defer_fetch(url, site_id, is_index=False):

    site_config = fetch_config[site_id]
    if is_index:
        result = urlfetch.fetch(url)
        news_url = get_news_urls(site_id, result.content.decode(site_config["encoding"]).encode('utf-8'))
        for _url in news_url:
            taskqueue.add(url='/start_fetch', params={'url': _url, 'site_id': site_id})
    else:
        # contents includes: title, content
        if site_id in ('jwc',):
            result = urlfetch.fetch(url)
            contents = parse_page(result.content)
        else:
            # 以下是 readability parser api 的输出示例
            # http://www.readability.com/api/content/v1/parser?url=http://news.scu.edu.cn/news2012/cdzx/webinfo/2013/03/1343288896620954.htm&token=16208e14fab764c70989011f1f26fc8c71b85451
            result = urlfetch.fetch("http://www.readability.com/api/content/v1/parser?url="\
             + url\
                  + "&token=16208e14fab764c70989011f1f26fc8c71b85451")
            contents = result.content
            contents = json.loads(contents)
            p = PageContent(url=url, site_id=site_id, title=contents['title'], content=contents['content'])
            p.put()



def parse_page(page_content):
    pass

def get_news_urls(site_id, content):
    site_config = fetch_config[site_id]
    soup = bs(content)
    urls = soup.findAll('a', href=re.compile(site_config['url_pattern']))
    urls = map(lambda x: urlparse.urljoin(site_config['prefix_url'], x['href']), urls)
    return urls




app = webapp2.WSGIApplication([
    ('/start_fetch', FetchHandler)
], debug=True)


##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

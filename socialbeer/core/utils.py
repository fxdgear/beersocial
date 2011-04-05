import re
from lxml import etree
from httplib2 import Http
from urllib import urlencode

def expand_urls(text, *args, **kwargs):
    urls = re.findall(r'(https?://\S+)', text)
    if urls:
        for url in urls:
            h = Http()
            api_url = "http://api.longurl.org/v2/expand"
            params = urlencode({"url":url})
            r,c = h.request(("%s?%s"%(api_url,params)), "GET")
            if r.status == 200:
                x = etree.XML(c)
                results = x.xpath("/response/long-url/text()")
                if results:
                    text = text.replace(url, results[0])

    return text

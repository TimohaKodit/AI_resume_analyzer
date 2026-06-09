import feedparser


feeds = [
    "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://feeds.feedburner.com/TechCrunch",
]
def fetch(url):
    feed = feedparser.parse(url)
    stat = []
    for i in feed.entries:
        stat.append({'title': i.title, 'link': i.link})
    return stat


def fetch_all(feeds):
    result = []
    for i in feeds:
        result.extend(fetch(i))
    return result

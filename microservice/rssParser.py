import feedparser
import asyncio
from rich.pretty import pprint as print
import datetime

rss_map = {
    'Новости Интерфакс': 1,
    'ПРАЙМ': 2,
    'Opennet': 3 
}

def addToDB(**kwargs):
    try:
        cursor = kwargs['db'].cursor()
        kwargs['title'] = kwargs['title'].replace('"', '').replace("'", '')
        select_by_title = 'select * from article where title = "%s";' % kwargs["title"]
        cursor.execute(select_by_title)
        records = cursor.fetchall()
        if records == []:
            add_article = ("INSERT INTO article "
                           "(title, content, datetime, id_source) "
                           "VALUES (%s, %s, %s, %s);")
            cursor.execute(add_article, (kwargs['title'],
                                        kwargs['content'],
                                        kwargs['date'],
                                        kwargs['source']))
            kwargs['db'].commit()
            print(kwargs)
        cursor.close()
    except Exception as e:
        print(e)


async def rssParser(source, url, db):
    while True:

        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            if 'summary' not in entry and 'title' not in entry:
                continue
        
            title = entry['title'] if 'title' in entry else ''
            link = entry['link'] if 'link' in entry else ''

            addToDB(
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                title = title,
                content = link,
                source = rss_map[source],
                db = db)

        await asyncio.sleep(20)

if __name__ == "__main__":
    a = rssParser('https://www.opennet.ru/opennews/opennews_all_utf.rss')

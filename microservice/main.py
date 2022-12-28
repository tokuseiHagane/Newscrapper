import httpx
import asyncio
from rich.pretty import pprint as print
# from telegram_parser import telegram_parser
from tgParser import tgParser
from rssParser import rssParser
from config import api_id, api_hash
import mysql.connector


while True:
    try:
        db = mysql.connector.connect(host = 'db', user = 'root', password = 'example', port = 3306, database = 'appdb')
        break
    except Exception as e:
        print(f'{e}')
tg_channels = (
        'https://t.me/rbc_news',
        'https://t.me/rt_russian',
        'https://t.me/rian_ru',
        'https://t.me/boris_rozhin'
)

rss_channels = {
    'ПРАЙМ': 'https://1prime.ru/export/rss2/index.xml',
    'Новости Интерфакс': 'https://www.interfax.ru/rss.asp',
    'Opennet': 'https://www.opennet.ru/opennews/opennews_full.rss'
}
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Телеграм парсер
client = tgParser('session', api_id, api_hash, tg_channels, db)
httpx_client = httpx.AsyncClient()
# Добавляй в текущий event_loop rss парсеры
for source, rss_link in rss_channels.items():

    # https://docs.python-guide.org/writing/gotchas/#late-binding-closures
    async def wrapper(source, rss_link, db):
        try:
            await rssParser(source, rss_link, db)
        except Exception as e:
            print(f'&#9888; ERROR: {source} parser is down! \n{e}')

    loop.create_task(wrapper(source, rss_link, db))


try:
    # Запускает все парсеры
    client.run_until_disconnected()
except Exception as e:
    message = f'&#9888; ERROR: telegram parser (all parsers) is down! \n{e}'
finally:
    loop.run_until_complete(httpx_client.aclose())
    loop.close()

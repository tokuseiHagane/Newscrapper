from telethon import TelegramClient, events
import asyncio
from config import api_id, api_hash
from rich.pretty import pprint as print


tg_map = {
    "РБК": 4,
    "РИА Новости": 5,
    'RT на русском': 6,
    'Colonelcassad': 7
}

def addToDB(**kwargs):
    try:
        kwargs['content'] = kwargs['content'].replace('"', '').replace("'", '')
        cursor = kwargs['db'].cursor()
        add_article = ("INSERT INTO article "
                "(title, content, datetime, id_source) "
                "VALUES (%s, %s, %s, %s);")
        cursor.execute(add_article, (kwargs['title'],
                                    kwargs['content'],
                                    kwargs['date'],
                                    kwargs['source']))
        kwargs['db'].commit()
        cursor.close()
    except Exception as e:
        print(e)


def tgParser(session, api_id, api_hash, tg_channels, db):

    client = TelegramClient(session, api_id, api_hash)
    client.start()

    @client.on(events.NewMessage(chats=tg_channels))
    async def handler(event):
        msg = event.message

        link = await client.get_entity(msg.peer_id.channel_id)
        link = f'https://t.me/{link.username}/{msg.id}'

        addToDB(
            date = msg.date.strftime('%Y-%m-%d %H:%M:%S'),
            title = None,
            content = event.raw_text + f'\n\n{link}',
            source = tg_map[msg.chat.title],
            db = db)
        db.commit()

    return client

if __name__ == "__main__":

    client = tgParser('session', api_id, api_hash, (
        'https://t.me/rbc_news',
        'https://t.me/rt_russian',
        'https://t.me/rian_ru',
        'https://t.me/boris_rozhin'))
    client.run_until_disconnected()

import random
import asyncio
from collections import deque
from telethon import TelegramClient, events

from config import api_id, api_hash
import httpx
import feedparser

from utils import random_user_agent_headers

telegram_channels: dict = {}
async def rss_parser(httpx_client, source, rss_link, posted_q, n_test_chars=50, 
                 timeout=2, check_pattern_func=None, 
                 send_message_func=None, logger=None):
    '''Парсер rss ленты'''
    while True:
        try:
            response = await httpx_client.get(rss_link, headers=random_user_agent_headers())
            response.raise_for_status()
        except Exception as e:
            if logger is not None:
                logger.error(f'{source} rss error pass\n{e}')
            await asyncio.sleep(timeout*2 - random.uniform(0, 0.5))
            continue
        feed = feedparser.parse(response.text)
        for entry in feed.entries[:20][::-1]:
            if 'summary' not in entry and 'tittle' not in entry:
                continue
            summary = entry['summary'] if 'summary' in entry else ''
            title = entry['title'] if 'title' in entry else ''
            news_text = f'{title}\n{summary}'
            if not (check_pattern_func is None):
                if not check_pattern_func(news_text):
                    continue
            head = news_text[:n_test_chars].strip()
            if head in posted_q:
                continue
            link = entry['link'] if 'link' in entry else ''
            post = f'<b>{source}</b>\n{link}\n{news_text}'
            if send_message_func is None:
                print(post, '\n')
            else:
                await send_message_func(post)
            posted_q.appendleft(head)
        await asyncio.sleep(timeout - random.uniform(0, 0.5))


def telegram_parser(session, api_id, api_hash, telegram_channels, posted_q,
                n_test_chars=50, check_pattern_func=None,
                send_message_func=None, logger=None, loop=None):
    '''Телеграм парсер'''
    # Ссылки на телеграмм каналы
    telegram_channels_links = list(telegram_channels.values())
    client = TelegramClient(session, api_id, api_hash,
                            base_logger=logger, loop=loop)
    client.start()
    @client.on(events.NewMessage(chats=telegram_channels_links))
    async def handler(event):
        '''Забирает посты из телеграмм каналов и посылает их в наш канал'''
        if event.raw_text == '':
            return
        news_text = ' '.join(event.raw_text.split('\n')[:2])
        if not (check_pattern_func is None):
            if not check_pattern_func(news_text):
                return
        head = news_text[:n_test_chars].strip()
        if head in posted_q:
            return
        source = telegram_channels[event.message.peer_id.channel_id]
        link = f'{source}/{event.message.id}'
        channel = '@' + source.split('/')[-1]
        post = f'<b>{channel}</b>\n{link}\n{news_text}'
        if send_message_func is None:
            print(post, '\n')
        else:
            await send_message_func(post)
        posted_q.appendleft(head)
    return client

    
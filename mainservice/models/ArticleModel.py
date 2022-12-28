import datetime
from app.models.SourceModel import Source
from rich.pretty import pprint as print

class Article:
    source = Source()
    sources_model = None
    source_keys = ['id', 'name']

    def get_articles(self, db, start_time=None, time_range=-1, sources=[1,2,3,4,5,6,7], source_types=["tg", "rss"], offset=0) -> list:
        self.sources_model = self.source.get_sources(db) if self.sources_model is None else self.sources_model
        self.sources_model = [{record[0]:record[1]} for record in self.sources_model]
        cursor = db.cursor()
        start_time = datetime.datetime.fromtimestamp(start_time)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        sources_str = ','.join([str(s) for s in sources])

        types = ','.join(source_types)
        types_map = {
            'tg,rss': '"tg","rss"',
            'tg': '"tg"',
            'rss': '"rss"'
        }
        if start_time != None:
            if time_range == -1:
                sql_query = 'select a.*, s.source_type from article as a join source as s on a.id_source = s.id' \
                            f' and s.source_type in ({types_map[types]}) and a.id_source in ({sources_str})' \
                            f' where a.datetime <= "{start_time_str}"' \
                            f' order by a.datetime desc limit {offset*10 + 1}, 10;'
            else:
                end_time = start_time - datetime.timedelta(days=time_range)
                end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
                sql_query = 'select a.*, s.source_type from article as a join source as s on a.id_source = s.id' \
                            f' and s.source_type in ({types_map[types]}) and a.id_source in ({sources_str})' \
                            f' where a.datetime <= "{start_time_str}" and a.datetime > "{end_time_str}"' \
                            f' order by a.datetime desc limit {offset*10 + 1}, 10;'
        else:
            sql_query = 'select a.*, s.source_type from article as a join source as s on a.id_source = s.id' \
                        f' and s.source_type in ({types_map[types]}) and a.id_source in ({sources_str}) and' \
                        f' order by a.datetime desc limit {offset*10 + 1}, 10;'
        cursor.execute(sql_query)
        records = cursor.fetchall()
        cursor.close()
        record_keys = ['id', 'title', 'content', 'datetime', 'source', 'source_type']
        records = [{record_keys[i]:record[i] for i in range(len(record_keys))} for record in records]
        
        for record in records:

            if record['source_type'] == 'tg':
                record['source'] = self.sources_model[record['source']]
                record['source_type'] = 'Tg'
                record['info_class'] = 'news_info_tg'
                record['news_div'] = 'news_tg'
                record['setting'] = 'tg_setting'
                record['title'] = ''
            else:
                record['source'] = self.sources_model[record['source']]
                record['source_type'] = 'RSS'
                record['info_class'] = 'news_info_rss'
                record['news_div'] = 'news_rss'
                record['setting'] = 'rss_setting'
        print(records)
        return records
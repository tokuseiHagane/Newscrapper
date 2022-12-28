import datetime
from SourceModel import Source


class Article:
    source = Source()


    def get_articles(self, db, start_time, time_range, sources, source_types, offset=0) -> list:
        cursor = db.cursor()
        start_time = datetime.datetime.fromtimestamp(start_time)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        sources_str = ','.join([str(s) for s in sources])
        types = ','.join(source_types)
        if time_range == -1:
            sql_query = 'select a.*, s.source_type from article as a join source as s on a.id_source = s.id' \
                        f'and s.source_type in ({types}) and a.id_source in ({sources_str})' \
                        f'where a.datetime >= "{start_time_str}"' \
                        f'order by a.datetime desc offset {offset*5} limit 10;'
        else:
            end_time = start_time + datetime.timedelta(days=time_range)
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
            sql_query = 'select a.*, s.source_type from article as a join source as s on a.id_source = s.id' \
                        f'and s.source_type in ({types}) and a.id_source in ({sources_str})' \
                        f'where a.datetime >= "{start_time_str}" and a.datetime < "{end_time_str}"' \
                        f'order by a.datetime desc offset {offset*5} limit 10;'
        cursor.execute(sql_query)
        records = cursor.fetchall()
        return records
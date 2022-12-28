class Source:
    def get_sources(self, db):
        sql_query = 'select * from source;'
        cursor = db.cursor()
        cursor.execute(sql_query)
        records = cursor.fetchall()
        cursor.close()
        return records

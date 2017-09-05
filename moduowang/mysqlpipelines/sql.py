import mysql.connector
from moduowang import settings

MYSQL_HOSTS = settings.MYSQL_HOST
MYSQL_DB = settings.MYSQL_DB
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWD
MYSQL_PORT = settings.MYSQL_PORT

conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cursor = conn.cursor(buffered=True)

class Sql:
    @classmethod
    def insert_into_table(cls, item):
        sql = "insert into moduo(id, name, url, tag, time) VALUES (%s, %s, %s, %s, %s)"
        params = (item['url'][0].split('/')[-1].split('.')[0], item['name'][0], item['url'][0], item['tag'][0], item['time'][0])
        cursor.execute(sql, params)
        conn.commit()

    @classmethod
    def select_url_id(cls, url):
        sql = 'select exists(select 1 from moduo where url = %(url)s)'
        value = {
            'url': url
        }
        cursor.execute(sql, value)
        return cursor.fetchall()[0]
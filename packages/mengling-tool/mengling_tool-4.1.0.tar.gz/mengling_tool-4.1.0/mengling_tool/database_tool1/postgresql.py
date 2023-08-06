import psycopg2
from .__sqltool__ import TemplateSQLTool, decrypt
import traceback


# postgresql执行类
class PostgresqlExecutor(TemplateSQLTool):
    def __init__(self, dbname: str, **connect):
        self.dbname = dbname
        self.connect = connect
        self.host = connect.get('host', '127.0.0.1')
        self.port = connect.get('port', 5432)
        self.user = connect.get('user', 'postgres')
        self.passwd = connect['passwd']
        self.charset = connect.get('charset', 'UTF8')
        ifassert = connect.get('ifassert', False)
        iftz = connect.get('iftz', False)
        self.ifencryption = connect.get('ifencryption', True)
        if self.ifencryption and self.user != 'postgres':
            self.passwd = decrypt(self.user, self.passwd)
        # 打开数据库连接
        self.db = psycopg2.connect(host=self.host, port=self.port,
                                   user=self.user, password=self.passwd,
                                   database=self.dbname)
        self.db.set_client_encoding(self.charset)
        self.cursor = self.db.cursor()
        TemplateSQLTool.__init__(self, self.db, self.cursor, connect, ifassert, iftz)

    def getTablestr(self, table, **kwargs):
        if '.' in table:
            t1, t2 = table.split('.')
            return '"%s"."%s"' % (t1, t2)
        else:
            return '"%s"' % table

    def getLiestrs(self, lies, **kwargs):
        if lies == '*' or lies == 'count(1)':
            return [lies]
        else:
            if type(lies) == str: lies = [lies]
            lies = [('"%s"' % lie.replace('%', '%%')) for lie in lies]
            return lies

    def getValuestrs(self, values, **kwargs):
        valuestrs = ["'%s'" % str(value).replace("'", "\\'").strip() for value in values]
        return valuestrs


if __name__ == "__main__":
    import config, json

    sqltool = PostgresqlExecutor('ymx', **config.POSTGRESQL_CONNECT)
    txt = '''
    [
      {
        "value": "yes",
        "note": "Low Beam Headlight\u00ef\u00bc\u009bAmazon filter system may not be 100% accurate\u00ef\u00bc\u008cPlease check owners manual confirm bulb size before placing an order.  Or you can ask us,We will help you choose the right bulb.",
        "positions": "Low Beam",
        "link": "https://www.amazon.ca/gp/part-finder-ajax/asCheckFit.html?year=2007&makeId=72&modelId=939&asin=B079KCGWLM",
        "sku": "AHDS19006-E",
        "cartype": "automotive",
        "web": "ca",
        "asin": "B079KCGWLM",
        "year": "2007",
        "make": "Mitsubishi",
        "model": "Galant"
      }
    ]
    '''
    a = json.loads(txt)
    sqltool.insert_create_dt('组合.temp', *a, columnclassdict={'note': 'text'}, key='link')
    sqltool.commit()
    sqltool.close()

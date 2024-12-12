import pymysql
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO)

# MySQL 数据库配置信息
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWD = "Mysql541880!"
MYSQL_DB = "chatmooc"

class MysqlDb:
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=10
            )
            self.cur = self.conn.cursor()
            logging.info("Database connection established")
        except pymysql.MySQLError as e:
            logging.error(f"Error connecting to the database: {e}")
            self.conn = None
            self.cur = None

    def ensure_connection(self):
        try:
            if self.conn is None or self.cur is None or not self.conn.open:
                self.connect()
            else:
                self.conn.ping(reconnect=True)
        except pymysql.MySQLError as e:
            logging.error(f"Error pinging database: {e}")
            self.connect()

    def select_db(self, sql):
        """查询"""
        self.ensure_connection()
        if self.conn is None or self.cur is None:
            logging.error("Database connection is not available")
            return None
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            return data
        except pymysql.MySQLError as e:
            logging.error(f"Error executing query: {e}")
            return None

    def __del__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logging.info("Database connection closed")

    def execute_db(self, sql, params=None):
        """更新/新增/删除"""
        self.ensure_connection()
        if self.conn is None or self.cur is None:
            logging.error("Database connection is not available")
            return "操作失败: 数据库连接不可用"
        try:
            if params:
                self.cur.execute(sql, params)
            else:
                self.cur.execute(sql)
            self.conn.commit()
            return "操作成功"
        except pymysql.MySQLError as e:
            self.conn.rollback()
            logging.error(f"Error executing query: {e}")
            return f"操作出现错误: {e}"


# 定义一个实例对象，方便别的文件引用其方法
db = MysqlDb(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB)

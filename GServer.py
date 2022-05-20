import pymysql


class Server:

    def __init__(self):
        self.__conn = None
        self.__dbInfo = None

    def connectDB(self):
        self.__conn = pymysql.connect(
            host=self.__dbInfo['host'],
            user=self.__dbInfo['user'],
            password=self.__dbInfo['password'],
            db=self.__dbInfo['db'],
            charset=self.__dbInfo['charset'],
        )

    def setDBInfo(self, db_info: dict):
        self.__dbInfo = db_info

    def getDBInfo(self) -> dict:
        return self.__dbInfo

    def showInfo(self):
        cur = self.__conn.cursor()
        SQL = """select * from stu_info;"""
        cur.execute(SQL)
        data = cur.fetchall()
        print(data)

    def run(self):
        pass


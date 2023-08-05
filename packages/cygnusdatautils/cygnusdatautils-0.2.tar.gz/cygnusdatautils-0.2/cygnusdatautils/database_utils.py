from psycopg2 import connect

class DatabaseUtils():
    def __int__(self):
        self.name = 'database_utils'

    def connect_postgresql_database(self, host, port, username, password, database):
        conn = connect(
            "dbname={} user={} password={} host={} port={}".format(database, username, password, host, port))
        return conn
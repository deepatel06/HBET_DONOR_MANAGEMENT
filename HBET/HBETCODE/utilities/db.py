import pymysql

def get_db_connection():
    try:
        conn = pymysql.connect(
            db = 'Hbet',
            user = 'root',
            password = '@Vvp150470',
            host = '127.0.0.1',
            connect_timeout=500
        )
    except pymysql.MySQLError as e:
        print(e)
    return conn


def close_connection(conn):
    print("Closing db connection")
    conn.close()
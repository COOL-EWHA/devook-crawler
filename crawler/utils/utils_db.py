import MySQLdb


def connect_db(user, passwd, host, db):
    return MySQLdb.connect(user=user, passwd=passwd, host=host, db=db)


def disconnect_db(conn):
    conn.commit()
    conn.close()


def insert_into_database(items, user, passwd, host, db):
    conn = connect_db(user=user, passwd=passwd, host=host, db=db)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS post")  # 해당 테이블이 이미 존재할 경우 삭제
    cursor.execute(
        "CREATE TABLE post "
        "(id            int AUTO_INCREMENT PRIMARY KEY, "
        "url            text, "
        "title          text, "
        "description    text, "
        "category       text)"
    )  # 새로운 테이블 생성

    sql = "INSERT INTO post(url, title, description, category) VALUES(%s, %s, %s, %s)"
    for item in items:
        values = (item[0], item[1], item[2], item[3])
        cursor.execute(sql, values)

    disconnect_db(conn=conn)

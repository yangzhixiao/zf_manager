import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


global conn


def connect():
    global conn
    conn = sqlite3.connect('./zf.db', check_same_thread=False)
    conn.row_factory = dict_factory


def query(sql, *args):
    if conn is None:
        connect()
    cursor = conn.cursor()
    values = None
    try:
        cursor.execute(sql, args)
        values = cursor.fetchall()
        cursor.close()
        conn.commit()
    except Exception as ex:
        print(ex.__str__())
        cursor.close()
    return values


def query_one(sql, *args):
    if conn is None:
        connect()
    cursor = conn.cursor()
    value = None
    try:
        cursor.execute(sql, args)
        value = cursor.fetchone()
        cursor.close()
        conn.commit()
    except Exception as ex:
        print(ex.__str__())
        cursor.close()
    return value


def query_count(sql, *args):
    if conn is None:
        connect()
    cursor = conn.cursor()
    value = None
    try:
        cursor.execute(sql, args)
        value = cursor.fetchone()
        cursor.close()
        conn.commit()
        keys = value.keys()
        return value[list(keys)[0]]
    except Exception as ex:
        print(ex.__str__())
        cursor.close()
    return value


def execute(sql, *args):
    if conn is None:
        connect()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, args)
        rowcount = cursor.rowcount
        cursor.close()
        conn.commit()
        return rowcount
    except Exception as ex:
        print(ex.__str__())
        cursor.close()
        return None


def close():
    if conn is not None:
        conn.close()

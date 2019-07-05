import sqlite3

conn = sqlite3.connect('./zf.db')


def query(sql, *args):
    cursor = conn.cursor()
    cursor.execute(sql, args)
    values = cursor.fetchall()
    cursor.close()
    conn.commit()
    return values


def query_one(sql, *args):
    cursor = conn.cursor()
    cursor.execute(sql, args)
    value = cursor.fetchone()
    cursor.close()
    conn.commit()
    return value


def query_count(sql, *args):
    cursor = conn.cursor()
    cursor.execute(sql, args)
    value = cursor.fetchone()
    cursor.close()
    conn.commit()
    return value[0]


def execute(sql, *args):
    cursor = conn.cursor()
    cursor.execute(sql, args)
    rowcount = cursor.rowcount
    cursor.close()
    conn.commit()
    return rowcount


def close():
    conn.close()

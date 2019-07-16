import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect('./zf.db', check_same_thread=False)
conn.row_factory = dict_factory


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
    keys = value.keys()
    return value[list(keys)[0]]


def execute(sql, *args):
    cursor = conn.cursor()
    cursor.execute(sql, args)
    rowcount = cursor.rowcount
    cursor.close()
    conn.commit()
    return rowcount


def close():
    conn.close()

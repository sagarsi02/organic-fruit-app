from django.db import connections


def my_custom_sql(query, params=None, fetchone=False, db_name='default'):
    with connections[db_name].cursor() as cursor:
        cursor.execute(query, params)
        if fetchone:
            return dictfetchone(cursor)
        return dictfetchall(cursor)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if not row:
        return {}
    return dict(zip(columns, row))

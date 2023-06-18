import psycopg2


class Database:
    def __init__(self, host, port, dbname, user, password):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

    def connect(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password
        )

    def execute_query(self, query, params=None):
        conn = self.connect()
        cur = conn.cursor()

        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

        if query.__contains__('CALL'):
            result = None
        else:
            result = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        return result

    def insert(self, table, columns, values):
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"
        return self.execute_query(query, values)

    def update(self, table, set_clause, where_clause=None, params=None):
        query = f"UPDATE {table} SET {set_clause}"
        if where_clause:
            query += f" WHERE {where_clause}"
        return self.execute_query(query, params)

    def delete(self, table, where_clause=None, params=None):
        query = f"DELETE FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        return self.execute_query(query, params)

    def select(self, table, columns="*", where_clause=None, params=None):
        query = f"SELECT {columns} FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        return self.execute_query(query, params)

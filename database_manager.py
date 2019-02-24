import sqlite3
from sqlite3 import Error
import os



class DbManager:
    """
    Database manager
    """


    def get_db_content(self, bot, tables=False, storage=False):
        """
        Get content from every table in the database
        :param bot: Chatterbot instante, provides connection to storage
        :param database: String, path to the SQLite database
        :param tables: Bool, showcase list of tables
        :param storage: Boo, showcase number of items in database
        :return:
        """
        # Tag, statement, tag_association
        db_path = bot.storage.database_uri.rsplit('/', 1)[-1]  # Get name of the database
        db_path = os.path.join(os.getcwd(), db_path)  # Concat path with the name
        try:
            conn = sqlite3.connect(db_path)
        except Error as e:
            print(e)
            return None

        # Create cursor
        cur = conn.cursor()

        # Get content
        cur.execute("SELECT name FROM sqlite_master where type = 'table';")
        tables_info = cur.fetchall()

        # Get tables info
        if tables:
             print('Table list: ', tables_info)

        # Get tables info
        for table in tables_info:
            value = None
            cur.execute(f"SELECT * from {table[0]}")
            value = cur.fetchall()
            print(f"{table} has: ", value)

        # Get storage count
        if storage:
            print('Storage count: ', bot.storage.count())
        conn.close()
        return
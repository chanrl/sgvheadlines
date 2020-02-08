import sqlite3
from sqlite3 import Error
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create_table():
    database = r'db/sgvheadlines.db'
    sql_create_table = """ 
                    CREATE TABLE sgvheadlines(
                    id integer PRIMARY KEY,
                    headline text NOT NULL,
                    date text
                    );
                   """
    conn = create_connection(database)
    c = conn.cursor()
    c.execute(sql_create_table)

def create_headline(conn, headline):
    sql = ''' INSERT INTO sgvheadlines (headline, date)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, headline)
    return cur.lastrowid

def insert_headline(article_name, date):
    database = r"db/sgvheadlines.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # headline to insert
        headline = (article_name, date)
        headline_id = create_headline(conn, headline)
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_menu(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM menu")

    rows = cur.fetchall()

    #for row in rows:
        #print(row)

    return rows

def select_all_team(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM spieler WHERE nummer IS NOT NULL")

    rows = cur.fetchall()

    #for row in rows:
        #print(row)

    return rows

def confederations(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT name_verband, en FROM verbaende")

    rows = cur.fetchall()

    #for row in rows:
        #print(row)

    return rows

def select_taktiken(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT aufstellung FROM taktiken")

    rows = cur.fetchall()

    #for row in rows:
        #print(row)

    return rows

def select_stats(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT e.attribut, a.attributname, e.wert FROM eigenschaften e, attribute a WHERE e.attribut = a.id_attribut AND spieler = 2")

    rows = cur.fetchall()

    #for row in rows:
        #print(row)

    return rows

def select_dashboard(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM menu where dashboard=1 ORDER BY id_menu")

    rows = cur.fetchall()

    #for row in rows:
        #print(row)

    return rows

def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

def connect_goal_db():
    #database = r"C:\sqlite\db\pythonsqlite.db"
    database = r'database/GoalFM.db'

    # create a database connection
    conn = create_connection(database)
    with conn:
        #print("1. Query task by priority:")
        #select_task_by_priority(conn, 1)

        #print("2. Query all tasks")
        #select_all_tasks(conn)
        return conn

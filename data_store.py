import sqlite3

__connection = None
def get_connection():

    global __connection
    if __connection is None:
        __connection = sqlite3.connect('user.db')
    return __connection

def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS user_int
    (
   id_user INT PRIMARY KEY)
    """)
    conn.commit()

def create_table_off():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_off 
    (
	id_user_off INT PRIMARY KEY,
	id_user_int INTEGER NOT NULL,
	FOREIGN KEY (id_user_int) REFERENCES user_int (id_user)
	ON DELETE CASCADE)
	''')
    conn.commit()

def user_int_insert(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO user_int (id_user) 
values(?)
    """, (id,))
    conn.commit()

def user_int_off_insert(id, id_user):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""INSERT INTO user_off (id_user_off, id_user_int) 
values(?, ?)
    """, (id,id_user,))
    conn.commit()

def select_user_int():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT * FROM user_int''')
    id = c.fetchall()
    total = []
    for i in id:
        total.append(str(*i))
    return total


def select_user_int_count(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT COUNT(id_user_off) FROM user_off WHERE id_user_int = (?)''', (id,))
    id = c.fetchone()
    total = 0
    for i in id:
        total+=i
    return total

def select_user_int_off(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''SELECT id_user_off FROM user_off WHERE id_user_int = (?)''', (id,))
    id = c.fetchall()
    total = []
    for i in id:
        total.append(str(*i))
    return total






if __name__ == '__main__':
    # pass
    # create_table()
    # create_table_off()
    # print(select_user_int_off(767605949))
    # user_int_off_insert(78826800, 767605949)
    print(select_user_int_off(479056077))

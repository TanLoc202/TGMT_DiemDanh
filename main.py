import sqlite3

def create_database(name):
    conn = sqlite3.connect(name)
    return conn

def create_table(db, name, field, primary_key, foreign_key = []):
    cur = db.cursor()

    str_field =  ", ".join([key + ' ' + val for key, val in field])
    str_key = f"primary key({', '.join(primary_key)}) {''.join([f', foreign key({k1}) REFERENCES {t}({k2})' for k1, t, k2 in foreign_key])}"
    sql_commnad = f'''CREATE TABLE IF NOT EXISTS {name} ({str_field}, {str_key})'''
    cur.execute(sql_commnad)

def insert(db, table, key, value):
    cur = db.cursor()
    cur.execute(f"INSERT INTO {table} ({''}) VALUES (?, ?)")

if __name__=="__main__":
    db = create_database("loc.db")
    create_table(db, "class", [['id_class', 'int'], ['name_class', 'text']], ['id_class'])
    create_table(db, "user", [['id', 'int'], ['name', 'text'], ['class', 'int']], ['id'], [['class', 'class', 'id_class']])
import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def get_db():
    
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), fetch=False, one=False):
    
    cur = None
    db = get_db()
    
    try:
        cur = db.execute(query, args)
        if fetch:
            rv = cur.fetchall()
            if rv is None:
                return None
            
            results = [dict(row) for row in rv]
            
            if one:
                return results[0] if results else None
            else:
                return results
        
        else:
            db.commit()
            
            if query.strip().upper().startswith("INSERT"):
                return cur.lastrowid
            

    except sqlite3.Error as e:
        db.rollback()
        print(f"Erreur SQL: {e}")
        raise e 
       
    finally:
        if cur:
            cur.close()


def init_db():
    
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@click.command('init-db')
def init_db_command():
    
    init_db()
    print('Initialized the database.')


def init_app(app):
    
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


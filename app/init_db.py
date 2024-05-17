import os
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

def init_session():
    engine = create_engine("sqlite:///app/bank.db", echo=False)
    try: 
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(e)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session



def get_database(func):
    """Decorateur qui initialise la connexion avec la bdd, lance une action sur la bdd puis ferme la connexion"""

    def wrap(*args, **kargs):
        path = os.path.dirname(os.path.abspath(__file__))
        db = os.path.join(path, "bank.db")
        con = sqlite3.connect(db)
        cur = con.cursor()
        result = func(*args, *kargs, cur)
        con.commit()
        con.close()
        return result
    return wrap


@get_database
def create_table(cur):
    """Crée les tables accounts et transactions"""

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "accounts" (
            "id" INTEGER,
            "name" TEXT NOT NULL,
            "balance" REAL NOT NULL CHECK("balance" >= 0),
            PRIMARY KEY("id")
        );
                
        CREATE TABLE IF NOT EXISTS "transactions" (
            "id" INTEGER,
            "type" TEXT NOT NULL CHECK("type" IN 'deposit', 'withdraw', 'transfer'),
            "amount" REAL NOT NULL CHECK("amount" >= 0),
            "datetime" NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "initiator_account_id" INTEGER NOT NULL, 
            "receiver_account_id" INTEGER,
            PRIMARY KEY("id")
            FOREIGN KEY("initiative_account_id") REFERENCES "accounts"("id"),
            FOREIGN KEY("receiving_account_id") REFERENCES "accounts"("id")
        );
    """)
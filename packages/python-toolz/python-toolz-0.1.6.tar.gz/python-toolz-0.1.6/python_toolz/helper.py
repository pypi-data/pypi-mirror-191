from zpy_database import database as db


def database(conf):
    db.connect(conf)
    return db


def log(txt):
    print(txt)

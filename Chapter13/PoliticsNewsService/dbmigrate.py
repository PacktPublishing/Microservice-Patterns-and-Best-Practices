import os
from models import Base
from sqlalchemy import create_engine


def create_db():
    db = create_engine(os.environ.get("COMMANDDB_HOST"))
    db.execute('CREATE SEQUENCE IF NOT EXISTS news_id_seq START 1;')
    Base.metadata.create_all(db)


if __name__ == '__main__':
    print('creating databases')
    create_db()
    print('databases created')

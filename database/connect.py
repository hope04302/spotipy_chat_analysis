import os
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import scoped_session, sessionmaker
import atexit

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = 'database.db'
engine = create_engine(f'sqlite:///{BASE_DIR}/{DB_NAME}', echo=True)

session = scoped_session(
        sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=engine
        )
    )
print(session())


def delete_database_file():
    db_path = f'{BASE_DIR}/{DB_NAME}'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Deleted database file: {db_path}")
    else:
        print(f"Database file not found: {db_path}")


# 프로그램 종료 시 삭제 함수 등록
atexit.register(delete_database_file)

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connect, connection_record):
#     cursor = dbapi_connect.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()

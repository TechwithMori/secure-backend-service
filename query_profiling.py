from app import db, SecurityRecord
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    logging.debug("Query: %s", statement)
    logging.debug("Total Time: %f", total)

# Function to test and optimize queries
def test_queries():
    # Example optimized query using indexed column 'name'
    records = SecurityRecord.query.filter(SecurityRecord.name == 'example').all()
    for record in records:
        logging.debug(f"Record ID: {record.id}, Name: {record.name}, Description: {record.description}, Timestamp: {record.timestamp}")

if __name__ == '__main__':
    with db.engine.connect() as connection:
        connection.execute('pragma foreign_keys=ON')  # Enable foreign keys in SQLite
        test_queries()

import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('timescaledb://user:password@0.0.0.0:8001/database')
metadata = MetaData()
metadata.bind = engine
Base = declarative_base()

table = Table(
    'students', metadata,
    Column('name', String),
    Column('lastname', String),
    Column(
        'timestamp', DateTime(timezone=True), default=datetime.datetime.now
    ),
    timescaledb_hypertable={
        'time_column_name': 'timestamp'
    }
)

metadata.create_all(engine)

def test_one():
    assert True == True

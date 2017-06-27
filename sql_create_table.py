# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, REAL, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker


from datetime import datetime

db_name = "common.db"

Base = declarative_base()

class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    desc_short = Column(String(50))
    desc_long = Column(String(250))

    def __repr__(self):
        return "<Device(id='{}', name='{}')>".format(self.id, self.name)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    desc = Column(String(500))

    def __repr__(self):
        return "<Tag(id='{}', name='{}')>".format(self.id, self.name)


class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('device.id'), default=1)
    device = relationship(Device)
    tag_id = Column(Integer, ForeignKey('tag.id'), default=1)
    tag = relationship(Tag)
    value = Column(REAL)
    stime = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return "<Data(id='{}', device='{}' tag='{}' )>".format(
            self.id, self.device_id, self.tag_id, )


engine = create_engine('sqlite:///{}'.format(db_name), echo=False)

DBSession = sessionmaker()
# DBSession.bind = engine
session = DBSession(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


def add_init_data():
    new_device = Device(name="XKinstr")
    session.add(new_device)

    for tag_name in ["CO2", "T"]:
        new_tag = Tag(name=tag_name)
        session.add(new_tag)

    session.commit()


def check_if_data_table_exists():
    if not engine.dialect.has_table(engine, 'data'):
        create_tables()
        print "create tables"
        add_init_data()
        print "fill init data"
    else:
        print "table already exists"

if __name__ == '__main__':
    # create_tables()
    # add_init_data()
    check_if_data_table_exists()
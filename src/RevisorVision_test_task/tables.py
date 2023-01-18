from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from uuid import uuid1

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    __table_args__ = (
        UniqueConstraint("id"),
        UniqueConstraint("username"),
    )
    id: str = sa.Column(sa.String, default=str(uuid1()), primary_key=True)
    created_at: str = sa.Column(sa.Date, default=datetime.utcnow())
    username: str = sa.Column(sa.String)
    password_hash: str = sa.Column(sa.String)


class Plates(Base):
    __tablename__ = 'Plates'
    __table_args__ = (
        UniqueConstraint("plate"),
        UniqueConstraint("plate_uuid"),
    )
    plate_uuid: str = sa.Column(sa.String, default=str(uuid1()), primary_key=True)
    plate: str = sa.Column(sa.String)
    created_at: str = sa.Column(sa.Date, default=datetime.utcnow())
    user_id: str = sa.Column(sa.String, sa.ForeignKey('Users.id'))

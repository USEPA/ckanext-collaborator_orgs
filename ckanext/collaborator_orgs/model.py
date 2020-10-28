# encoding: utf-8

import datetime
import uuid
import logging
from collections import OrderedDict

from sqlalchemy import orm, Column, Unicode, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from ckan.model.meta import metadata

log = logging.getLogger(__name__)


def make_uuid():
    return unicode(uuid.uuid4())


Base = declarative_base(metadata=metadata)


class PackageOrgMember(Base):
    __tablename__ = u'package_member_group_table'

    dataset_id = Column(Unicode, ForeignKey('package.id'), primary_key=True)
    org_id = Column(Unicode, ForeignKey('group.id'), primary_key = True)
    capacity = Column(Unicode, nullable=False)
    modified = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
        _dict = OrderedDict()
        table = orm.class_mapper(self.__class__).mapped_table
        for col in table.c:
            val = getattr(self, col.name)
            if isinstance(val, datetime.date):
                val = str(val)
            if isinstance(val, datetime.datetime):
                val = val.isoformat()
            _dict[col.name] = val
        return _dict


def create_tables():
    PackageOrgMember.__table__.create()

    log.info(u'Dataset collaborator organizations database tables created')

def drop_tables():
    PackageOrgMember.__table__.drop()

    log.info(u'Dataset collaborator organizations database tables dropped')


def tables_exist():
    
    return PackageOrgMember.__table__.exists()

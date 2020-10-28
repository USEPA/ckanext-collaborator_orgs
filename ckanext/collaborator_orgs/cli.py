# encoding: utf-8

import sys
import logging

import click

# from ckan.plugins.toolkit import CkanCommand


from ckanext.collaborator_orgs.model import tables_exist, create_tables, drop_tables


def get_commands():
    return [collaborator_orgs]


@click.group()
def collaborator_orgs():
    """Collaborator Organizations commands.
    """
    pass


@collaborator_orgs.command(short_help=u"Prepare database tables")
def init_db():
    if tables_exist():
        print(u'Dataset collaborators tables already exist')
        sys.exit(0)

    create_tables()

    print(u'Dataset collaborator organizations tables created')


@collaborator_orgs.command(name='remove-db', short_help=u"Prepare database tables")
def remove_db():
    if not tables_exist():
        print(u'Dataset collaborator organizations tables do not exist')
        sys.exit(0)

    drop_tables()
    print(u'Dataset collaborators tables removed')


@collaborator_orgs.command(name='reset-db', short_help=u"Reset database tables")
def reset_db():
    if not tables_exist():
        print(u'Dataset collaborator organizations tables do not exist')
        sys.exit(0)
    else:
        drop_tables()

    create_tables()
    print(u'Dataset collaborator organizations tables reset')

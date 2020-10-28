import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultPermissionLabels

import logging

from ckanext.collaborator_orgs import blueprint
from ckanext.collaborator_orgs.helpers import get_collaborator_orgs
from ckanext.collaborator_orgs.model import tables_exist
from ckanext.collaborator_orgs.logic import action, auth
from ckanext.collaborator_orgs.cli import get_commands

log = logging.getLogger(__name__)

class CollaboratorOrgsPlugin(plugins.SingletonPlugin, DefaultPermissionLabels):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IPermissionLabels)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IClick)

    # IConfigurer

    def update_config(self, config_):

        if not tables_exist():
            log.critical(u'''The dataset collaborator organizations extension requires a database setup. Please run the following to create the database tables:
            ckan collaborator_orgs init_db''')

        toolkit.add_template_directory(config_, 'templates')
        #toolkit.add_public_directory(config_, 'public')
        #toolkit.add_resource('fanstatic', 'collaborator_orgs')

    # IClick

    def get_commands(self):
        return get_commands()

    # IActions

    def get_actions(self):
        return {
            'package_collaborator_org_create': action.package_collaborator_org_create,
            'package_collaborator_org_delete': action.package_collaborator_org_delete,
            'package_collaborator_org_list': action.package_collaborator_org_list,
        }

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            'package_collaborator_org_create': auth.package_collaborator_org_create,
            'package_collaborator_org_delete': auth.package_collaborator_org_delete,
            'package_collaborator_org_list': auth.package_collaborator_org_list,
            'package_update': auth.package_update,
        }

    # IPermissionLabels

    def get_dataset_labels(self, dataset_obj):
        labels = super(CollaboratorOrgsPlugin, self).get_dataset_labels(dataset_obj)
        collaborator_orgs = toolkit.get_action('package_collaborator_org_list')(
            {'ignore_auth': True}, {'id': dataset_obj.id})
        labels.extend(u'member-%s' % o[u'org_id'] for o in collaborator_orgs)
        return labels

    def get_user_dataset_labels(self, user_obj):
        labels = super(CollaboratorOrgsPlugin, self).get_user_dataset_labels(user_obj)
        return labels

    # ITemplateHelpers

    def get_helpers(self):
        return {'collaborator_orgs_get_collaborators': get_collaborator_orgs}

    # IBlueprint
    def get_blueprint(self):
        return blueprint.collaborator_orgs

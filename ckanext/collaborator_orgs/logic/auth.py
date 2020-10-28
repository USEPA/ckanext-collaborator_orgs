from ckan.plugins import toolkit

import logging

import ckan.model as model

import ckan.logic as logic
from ckan.logic.auth import get_package_object
from ckan.logic.auth.get import package_collaborator_list
from ckan.logic.auth.create import package_collaborator_create
from ckan.logic.auth.delete import package_collaborator_delete

from ckan.authz import has_user_permission_for_group_or_org
from ckan.authz import get_roles_with_permission


from ckan.logic.auth.get import resource_show as core_resource_show


log = logging.getLogger()




def package_collaborator_org_create(context, data_dict):
    '''Checks if a user is allowed to add collaborators to a dataset

    Matches the user collaborator authorization logic
    '''
    return package_collaborator_create(context, data_dict)


def package_collaborator_org_delete(context, data_dict):
    '''Checks if a user is allowed to delete collaborators from a dataset

    Matches the user collaborator authorization logic
    '''
    return package_collaborator_delete(context, data_dict)


def package_collaborator_org_list(context, data_dict):
    '''Checks if a user is allowed to list collaborators from a dataset

    Matches the user collaborator authorization logic
    '''
    return package_collaborator_list(context, data_dict)


# Core overrides
@toolkit.chained_auth_function
def package_update(next_auth, context, data_dict):

    user_name = context.get('user')

    package = get_package_object(context, data_dict)

    collaborator_orgs = toolkit.get_action('package_collaborator_org_list')(
        {'ignore_auth': True}, {'id': package.id, 'capacity': 'editor'})

    for c in collaborator_orgs:

        if has_user_permission_for_group_or_org(c.get('org_id'), user_name, 'update_dataset'):
            return {'success': True}

    return next_auth(context, data_dict)



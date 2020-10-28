import ckan.plugins.toolkit as toolkit

def get_collaborator_orgs(package_dict):
    '''Return collaborators list.
    '''
    context = {'ignore_auth': True} #TODO
    data_dict = {'id': package_dict['id']}

    _collaborators = toolkit.get_action('package_collaborator_org_list')(context, data_dict)
    collaborators = []

    for collaborator in _collaborators:
        collaborators.append([collaborator['org_id'], collaborator['capacity'] ])

    return collaborators



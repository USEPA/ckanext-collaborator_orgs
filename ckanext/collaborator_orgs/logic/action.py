
import logging
import datetime

from ckan import model as core_model
from ckan import authz
from ckan.plugins import toolkit

from ckan.lib.search import rebuild

from ckanext.collaborator_orgs.model import PackageOrgMember

log = logging.getLogger(__name__)

ALLOWED_CAPACITIES = ('editor', 'member')

def package_collaborator_org_create(context, data_dict):
    '''Make a user a collaborator in a dataset.

    If the user is already a collaborator in the dataset then their
    capacity will be updated.

    Currently you must be an Admin on the dataset owner organization to
    manage collaborators.

    :param id: the id or name of the dataset
    :type id: string
    :param user_id: the id or name of the user to add or edit
    :type user_id: string
    :param capacity: the capacity of the membership. Must be either 'editor' or 'member'
    :type capacity: string

    :returns: the newly created (or updated) collaborator
    :rtype: dictionary

    '''
    model = context.get('model', core_model)

    dataset_id, org_id, capacity = toolkit.get_or_bust(data_dict,
        ['id', 'org_id', 'capacity'])
    
    dataset = model.Package.get(dataset_id)
    if not dataset:
        raise toolkit.ObjectNotFound('Dataset not found')

    toolkit.check_access('package_collaborator_org_create', context, data_dict)

    org = model.Group.get(org_id)
    if not org:
        raise toolkit.ObjectNotFound('Organization not found')

    if capacity not in ALLOWED_CAPACITIES:
        raise toolkit.ValidationError('Capacity must be one of "{}"'.format(', '.join(ALLOWED_CAPACITIES)))

    # Check if organization already exists
    member = model.Session.query(PackageOrgMember).\
        filter(PackageOrgMember.dataset_id == dataset.id).\
        filter(PackageOrgMember.org_id == org.id).one_or_none()
    if not member:
        member = PackageOrgMember(dataset_id=dataset.id, org_id=org.id)
    member.capacity = capacity
    member.modified = datetime.datetime.utcnow()

    model.Session.add(member)
    model.repo.commit()

    #Rebuild search index for package to reflect updated permissions
    rebuild(dataset_id)

    log.info('Organization {} added as collaborator in dataset {} ({})'.format( org.name, dataset.id, capacity))

    return member.as_dict()


def package_collaborator_org_delete(context, data_dict):
    '''Remove a collaborator from a dataset.

    Currently you must be an Admin on the dataset owner organization to
    manage collaborators.

    :param id: the id or name of the dataset
    :type id: string
    :param user_id: the id or name of the user to remove
    :type user_id: string

    '''
    model = context.get('model', core_model)

    dataset_id, org_id = toolkit.get_or_bust(data_dict, ['id', 'org_id'])
    dataset = model.Package.get(dataset_id)
    
    if not dataset:
        raise toolkit.ObjectNotFound('Dataset not found')

    toolkit.check_access('package_collaborator_org_delete', context, data_dict)

    member = model.Session.query(PackageOrgMember).\
        filter(PackageOrgMember.dataset_id == dataset.id).\
        filter(PackageOrgMember.org_id == org_id).one_or_none()
    
    if not member:
        raise toolkit.ObjectNotFound('{} is not a collaborator on dataset {}'.format(org_id, dataset_id))

    model.Session.delete(member)
    model.repo.commit()

    org = model.Group.get(org_id)

    # Rebuild search index for package to reflect updated permissions
    rebuild(dataset_id)

    log.info('Organization {} removed as collaborator from dataset {}'.format(org.name, dataset.id))
    

def package_collaborator_org_list(context, data_dict):
    '''Return the list of all collaborators for a given dataset.

    Currently you must be an Admin on the dataset owner organization to
    manage collaborators.

    :param id: the id or name of the dataset
    :type id: string
    :param capacity: (optional) If provided, only users with this capacity are
        returned
    :type capacity: string

    :returns: a list of collaborators, each a dict including the dataset and
        user id, the capacity and the last modified date
    :rtype: list of dictionaries

    '''
    model = context.get('model', core_model)

    dataset_id = toolkit.get_or_bust(data_dict,'id')
    dataset = model.Package.get(dataset_id)

    if not dataset:
        raise toolkit.ObjectNotFound('Dataset not found')

    toolkit.check_access('package_collaborator_org_list', context, data_dict)

    capacity = data_dict.get('capacity')
    if capacity and capacity not in ALLOWED_CAPACITIES:
        raise toolkit.ValidationError('Capacity must be one of "{}"'.format(', '.join(ALLOWED_CAPACITIES)))
    
    q = model.Session.query(PackageOrgMember).\
        filter(PackageOrgMember.dataset_id == dataset.id)

    if capacity:
        q = q.filter(PackageOrgMember.capacity == capacity)

    members = q.all()

    return [member.as_dict() for member in members]





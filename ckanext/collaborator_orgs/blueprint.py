from flask import Blueprint
from flask.views import MethodView

import ckan.plugins.toolkit as toolkit
import ckan.model as model
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.logic as logic


def collaborator_org_delete(id):
    context = {u'model': model, u'user': toolkit.c.user}

    try:
        org_id = toolkit.request.params.get(u'org_id')

        toolkit.get_action('package_collaborator_org_delete')(context, {
            'id': id,
            'org_id': org_id
        })
    except toolkit.NotAuthorized:
        message = u'Unauthorized to delete collaborators {0}'.format(id)
        return toolkit.abort(401, toolkit._(message))
    except toolkit.ObjectNotFound as e:
        return toolkit.abort(404, toolkit._(e.message))

    toolkit.h.flash_success(toolkit._('Organization removed from collaborators'))

    return toolkit.h.redirect_to(u'dataset.collaborators_read', id=id)


class CollaboratorOrgEditView(MethodView):
    def post(self, id):
        context = {u'model': model, u'user': toolkit.c.user}

        try:
            form_dict = logic.clean_dict(
                dictization_functions.unflatten(
                    logic.tuplize_dict(
                        logic.parse_params(toolkit.request.form))))

            org = toolkit.get_action('organization_show')(context, {'id':form_dict['org_id'] })

            data_dict = { 'id': id, 'org_id': org['id'], 'capacity': form_dict['capacity'] }

            toolkit.get_action('package_collaborator_org_create')(context, data_dict)
            toolkit.h.flash_success(toolkit._('Organization added to collaborators'))

        except dictization_functions.DataError:
            return toolkit.abort(400, _(u'Integrity Error'))
        except toolkit.NotAuthorized:
            message = u'Unauthorized to edit collaborators for dataset {0}'.format(dataset_id)
            return toolkit.abort(401, toolkit._(message))
        except toolkit.ObjectNotFound:
            return toolkit.abort(404, toolkit._(u'Resource not found'))
        except toolkit.ValidationError as e:
            toolkit.h.flash_error(e.error_summary)
        
        return toolkit.h.redirect_to(u'dataset.collaborators_read', id=id)

    def get(self, id):
        context = {u'model': model, u'user': toolkit.c.user}
        data_dict = {'id': id}

        try:
            toolkit.check_access(u'package_collaborator_list', context, data_dict)
            pkg_dict = toolkit.get_action('package_show')(context, data_dict)
        except toolkit.NotAuthorized:
            message = u'Unauthorized to read collaborators {0}'.format(id)
            return toolkit.abort(401, toolkit._(message))
        except toolkit.ObjectNotFound as e:
            return toolkit.abort(404, toolkit._(u'Resource not found'))


        org_id = toolkit.request.params.get(u'org_id')

        extra_vars = {
            'capacities': [ {'name': 'editor', 'value': 'editor'},
                            {'name': 'member', 'value': 'member'},
                            ],
            'capacity': 'member',
            'pkg_dict': pkg_dict }

        if org_id:

            org_dict = toolkit.get_action('organization_show')(context, {'id': org_id})

            extra_vars['org_id'] = org_id
            extra_vars['org_name'] =  org_dict.get('title')

            collaborators = toolkit.get_action('package_collaborator_org_list')(context, data_dict)

            for c in collaborators:
                if c['org_id'] == org_id:
                    extra_vars['capacity'] = c['capacity']

        return toolkit.render('package/collaborators/collaborator_org_new.html', extra_vars)


collaborator_orgs = Blueprint('collaborator_orgs', __name__)

# collaborator_orgs.add_url_rule(
#     rule=u'/dataset/collaborators/<dataset_id>',
#     endpoint='read',
#     view_func=collaborator_org_read, methods=['GET',]
#     )

collaborator_orgs.add_url_rule(
    rule=u'/dataset/collaborator_orgs/<id>/new',
    view_func=CollaboratorOrgEditView.as_view('new'),
    methods=['GET', 'POST',]
    )

collaborator_orgs.add_url_rule(
    rule=u'/dataset/collaborator_orgs/<id>/delete',
    endpoint='delete',
    view_func=collaborator_org_delete, methods=['GET', 'POST']
    )
    

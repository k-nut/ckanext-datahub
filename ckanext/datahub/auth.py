import ckan.lib.helpers as h
import ckan.model as model
import ckan.logic as logic
import ckan.new_authz as new_authz
from ckan.common import _

@logic.auth_sysadmins_check
def datahub_package_create(context, data_dict):
    from ckan.logic.auth.create import _check_group_auth

    if new_authz.is_sysadmin(context.get('user')):
        return {'success': True}

    user = context['user']
    if not new_authz.auth_is_registered_user():
        return {'success': False, 'msg': _('You must login to create a dataset')}
    else:
        check1 = new_authz.check_config_permission('create_dataset_if_not_in_organization') \
            or new_authz.check_config_permission('create_unowned_dataset')

        if not check1 and not new_authz.has_user_permission_for_some_org(user, 'create_dataset'):
            h.redirect_to('/pages/requesting-an-organization')

    if not check1:
        return {'success': False, 'msg': _('User %s not authorized to create packages') % user}

    check2 = _check_group_auth(context,data_dict)
    if not check2:
        return {'success': False, 'msg': _('User %s not authorized to edit these groups') % user}

    # If an organization is given are we able to add a dataset to it?
    data_dict = data_dict or {}
    org_id = data_dict.get('organization_id')
    if org_id and not new_authz.has_user_permission_for_group_or_org(
            org_id, user, 'create_dataset'):
        return {'success': False, 'msg': _('User %s not authorized to add dataset to this organization') % user}
    return {'success': True}



def package_delete(context, data_dict):
    if model.User.get(context.get('user')):
        return {'success': True}

    return {'success': False,
            'msg': 'You are not authorized to delete packages.'}


def resource_delete(context, data_dict):
    if model.User.get(context.get('user')):
        return {'success': True}

    return {'success': False,
            'msg': 'You are not authorized to delete resources.'}


"""
def datahub_package_create(context, data_dict):
    from ckan.logic.action.create import package_create as default_create
    from paste.deploy.converters import asbool

    usr = model.User.get(context.get('user'))
    if usr:
        moderation = not asbool(usr.extras.get('moderation', True))
        if moderation:
            return {'success': False,
                    'msg': 'Your user account is pending moderation.'}

    return default_create(context, data_dict)
"""
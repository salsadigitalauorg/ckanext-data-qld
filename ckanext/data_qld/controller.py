import ckan.lib.base as base
import ckan.model as model
import ckan.plugins as plugins
import ckan.lib.helpers as helpers
from ckan.common import request
import logging

import constants

log = logging.getLogger(__name__)
tk = plugins.toolkit
c = tk.c


def _get_errors_summary(errors):
    errors_summary = ''

    for key, error in errors.items():
        errors_summary = ', '.join(error)

    return errors_summary


class DataQldUI(base.BaseController):

    def _get_context(self):
        return {'model': model, 'session': model.Session,
                'user': c.user, 'auth_user_obj': c.userobj}
 
    def open(self, id):
        data_dict = {'id': id}
        context = self._get_context()

        # Basic intialization
        c.datarequest = {}
        try:
            tk.check_access(constants.OPEN_DATAREQUEST, context, data_dict)
            c.datarequest = tk.get_action(constants.SHOW_DATAREQUEST)(context, data_dict)

            if c.datarequest.get('closed', False) == False:
                tk.abort(403, tk._('This data request is already open'))
            else:
                data_dict = {}
                data_dict['id'] = id
                data_dict['accepted_dataset_id'] = c.datarequest.get('accepted_dataset_id', '')

                tk.get_action(constants.OPEN_DATAREQUEST)(context, data_dict)
                tk.redirect_to(helpers.url_for(controller='ckanext.datarequests.controllers.ui_controller:DataRequestsUI', action='show', id=data_dict['id']))
        except tk.ValidationError as e:
            log.warn(e)
            errors_summary = _get_errors_summary(e.error_dict)
            tk.abort(403, errors_summary)
        except tk.ObjectNotFound as e:
            log.warn(e)
            tk.abort(404, tk._('Data Request %s not found') % id)
        except tk.NotAuthorized as e:
            log.warn(e)
            tk.abort(403, tk._('You are not authorized to close the Data Request %s' % id))
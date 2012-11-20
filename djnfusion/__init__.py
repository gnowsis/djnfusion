import xmlrpclib
import logging

from django.contrib.auth.models import User
from django.core.urlresolvers import get_callable


from djnfusion import settings


key = settings.API_KEY
company = settings.COMPANY
server = xmlrpclib.ServerProxy("https://%s.infusionsoft.com:443/api/xmlrpc" % company);

fields = ["Id", settings.USER_ID_FIELD_NAME]


_log = logging.getLogger('djnfusion')


def _user_or_id(user, user_id):

    _log.debug("user_or_id: user = %s, user_id = %s", user, user_id)


    if user:
        try:
            user = User.objects.get(id=user.id)
        except User.DoesNotExist:
            _log.error("User with id %s not found.", user.id)
            raise
    else:
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                _log.error("User with id %s not found.", user_id)
                raise

    if not user:
        raise ValueError("No user specified.")

    return user



def _user_dict(user, create=False, update=False):

    data = {
        settings.USER_ID_FIELD_NAME: settings.USER_ID_VALUE_PREPROCESSOR(user.id),
        'Email': user.email,
        'FirstName': user.first_name,
        'LastName': user.last_name,
    }

    if create:
        data.update(settings.ADDITIONAL_USER_FIELD_PROVIDER_CREATE(user))
    if update:
        data.update(settings.ADDITIONAL_USER_FIELD_PROVIDER_UPDATE(user))

    _log.debug("User data: %s", data)

    return data


# *****************************************************************

def sync_user(user=None, user_id=None):

    if not settings.COMPANY or not settings.API_KEY:
        return # do nothing

    user = _user_or_id(user, user_id)
    _log.debug("Syncing user %s with CRM ...", user)

    # lookup user by id
    _log.debug("Searching for user: %s = %s", settings.USER_ID_FIELD_NAME, settings.USER_ID_VALUE_PREPROCESSOR(user.id))
    results = server.DataService.findByField(key, "Contact", 10, 0, settings.USER_ID_FIELD_NAME, settings.USER_ID_VALUE_PREPROCESSOR(user.id), fields);
    if len(results) > 1:
        raise ValueError("Found %s users in Infusionsoft for user id %s, not touching anything. Please fix this." % (len(results), user.id))

    if len(results) == 0:
        _log.debug("No users found, creating it.")
        result = add_user(user=user, user_id=user_id)
    else:
        infusionsoft_user = results[0]
        _log.debug("Found user id %s, updating user in InfusionSoft ...", infusionsoft_user)
        result = update_user(infusionsoft_user['Id'], user=user, user_id=user_id)

    if result:
        _log.debug("Success.")

    if settings.AUTO_OPTIN:
        
        _log.debug("Attempting to opt-in email ...")
        if optin_user(user=user):
            _log.debug("Opt-in succeeded.")
        else:
            _log.debug("Opt-in failed.")
        

    return True



def add_user(user=None, user_id=None):

    user = _user_or_id(user, user_id)
    server.ContactService.add(key, _user_dict(user, create=True))
    return True


def update_user(infusionsoft_user_id, user=None, user_id=None):

    user = _user_or_id(user, user_id)
    server.ContactService.update(key, infusionsoft_user_id, _user_dict(user, update=True))
    return True


def optin_user(user=None, user_id=None):

    if not settings.COMPANY or not settings.API_KEY:
        return # do nothing

    user = _user_or_id(user, user_id)
    _log.debug("optin_user for user %s", user)

    if settings.OPTIN_ONLY_IF_ACTIVE and not user.is_active:
        _log.debug("User is not active, not opting in.")
        return False

    if not user.email:
        _log.debug("No email address specified in user profile, not opting in.")
        return False

    _log.debug("User is active: %s", user.is_active)
    _log.debug("Actually performing opt-in ...")
    return server.APIEmailService.optIn(key, user.email, settings.OPTIN_MESSAGE)



# *****************************************************************

def daily_statistics(user=None, user_id=None):

    if not settings.COMPANY or not settings.API_KEY:
        return # do nothing

    if not settings.DAILY_USER_STATISTICS:
        return

    user = _user_or_id(user, user_id)    

    results = server.DataService.findByField(key, "Contact", 10, 0, settings.USER_ID_FIELD_NAME, settings.USER_ID_VALUE_PREPROCESSOR(user.id), fields)

    if len(results) == 0:
        raise ValueError("User %s not found in Infusionsoft, need to sync_user first." % user.id)

    if len(results) > 1:
        raise ValueError("Found %s users in Infusionsoft for user id %s, not touching anything. Please fix this." % (len(results), user.id))

    infusionsoft_user = results[0]

    stat_values = {}
    for stat_key, stat_callable_name in settings.DAILY_USER_STATISTICS.iteritems():
        stat_values[stat_key] = get_callable(stat_callable_name)(user)

    #print "updating user %s with values %s" % (infusionsoft_user['Id'], stat_values)
    server.ContactService.update(key, infusionsoft_user['Id'], stat_values)

    return True


from django.conf import settings

COMPANY = getattr(settings, 'DJNFUSION_COMPANY', None)
API_KEY = getattr(settings, 'DJNFUSION_API_KEY', None)

USER_ID_FIELD_NAME = '_%s' % getattr(settings, 'DJNFUSION_USERID_FIELD_NAME', 'djUserID')
USER_ID_VALUE_PREPROCESSOR = getattr(settings, 'DJNFUSION_USER_ID_VALUE_PREPROCESSOR', lambda id: unicode(id))
ADDITIONAL_USER_FIELD_PROVIDER_CREATE = getattr(settings, 'DJNFUSION_ADDITIONAL_USER_FIELD_PROVIDER_CREATE', lambda u: dict())
ADDITIONAL_USER_FIELD_PROVIDER_UPDATE = getattr(settings, 'DJNFUSION_ADDITIONAL_USER_FIELD_PROVIDER_UPDATE', lambda u: dict())

AUTO_OPTIN = getattr(settings, 'DJNFUSION_AUTO_OPTIN', False)
OPTIN_ONLY_IF_ACTIVE = getattr(settings, 'DJNFUSION_OPTIN_ONLY_IF_ACTIVE', True)
OPTIN_MESSAGE = getattr(settings, 'DJNFUSION_OPTIN_MESSAGE', 'Auto-optin through the Web application.')

DAILY_USER_STATISTICS = getattr(settings, 'DJNFUSION_DAILY_USER_STATISTICS', {})

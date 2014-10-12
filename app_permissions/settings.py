# ==============================================================================
# IMPORTS
# ==============================================================================
# Python
from __future__ import unicode_literals
from importlib import import_module

# Django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy


__all__ = ('app_permissions_settings', )


# ==============================================================================
# SETTINGS
# ==============================================================================
USER_SETTINGS = getattr(settings, 'APP_PERMISSIONS', {})
DEFAULT_SETTINGS = {
    'APP_PERMISSIONS_CONTENT_TYPE_NAME': 'app_permission',
    'APP_PERMISSIONS_MIDDLEWARE_ACTION': (
        'django.core.exceptions.PermissionDenied'
    ),
    'APP_PERMISSIONS_MIDDLEWARE_MESSAGE': ugettext_lazy(
        'You do not have sufficient privileges to view this application.'
    ),
    'PROTECTED_APPS': (),
}


class APISettings(dict):
    def __init__(self, default_settings, user_settings):
        default_settings.update(user_settings)
        super(APISettings, self).__init__(**default_settings)
        self.validate_dependencies()

    def __getattr__(self, item):
        return self[item]

    def validate_dependencies(self):
        # Make sure that if we are using the AppPermissionsMiddleware, that we
        #   have APP_PERMISSIONS_MIDDLEWARE_ACTION set
        if 'app_permissions.middleware.AppPermissionsMiddleware' in (
            settings.MIDDLEWARE_CLASSES
        ):
            if not self.APP_PERMISSIONS_MIDDLEWARE_ACTION:
                raise ImproperlyConfigured(
                    'APP_PERMISSIONS_MIDDLEWARE_ACTION is required when the '
                    'AppPermissionsMiddleware is in use.'
                )

            try:
                # Nod to tastypie's use of importlib.
                parts = self['APP_PERMISSIONS_MIDDLEWARE_ACTION'].rsplit('.', 1)
                module_path, class_name = parts
                module = import_module(module_path)
                self['APP_PERMISSIONS_MIDDLEWARE_ACTION'] = getattr(
                    module,
                    class_name
                )
            except (ImportError, AttributeError) as e:
                msg = (
                    'Could not import "{0}" for API setting '
                    '"APP_PERMISSIONS_MIDDLEWARE_ACTION". {1}: {2}.'.format(
                        self.APP_PERMISSIONS_MIDDLEWARE_ACTION,
                        e.__class__.__name__,
                        e
                    )
                )

                raise ImportError(msg)


app_permissions_settings = APISettings(DEFAULT_SETTINGS, USER_SETTINGS)

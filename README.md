django-app-permissions
======================

App-based permissions for Django.

Configuration
-------------
1. Add `app_permissions` to `settings.INSTALLED_APPS`.
2. Add `app_permissions.middleware.AppPermissionsMiddleware` to your `settings.MIDDLEWARE_CLASSES`.
3. Configure the `APP_PERMISSIONS` (see below).


APP_PERMISSIONS defaults
------------------------
    APP_PERMISSIONS = {
        'APP_PERMISSIONS_CONTENT_TYPE_NAME': 'app_permission',
        'APP_PERMISSIONS_MIDDLEWARE_ACTION': 'django.core.exceptions.PermissionDenied',
        'APP_PERMISSIONS_MIDDLEWARE_MESSAGE': ugettext_lazy(
            'You do not have sufficient privileges to view this application.'
        ),
        'PROTECTED_APPS': (),
    }

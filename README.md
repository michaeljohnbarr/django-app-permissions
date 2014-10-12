django-app-permissions
======================

App-based permissions for Django based off of URL patterns. In order for this to work, each application should have their URLs included as follows:

    urlpatterns = patterns('',
        url(r'^myapp/', include('myapp.urls', app_name='myapp')),
    )
    
The key here is the `app_name` argument in the includes. Without it, the `app_permissions.middleware.AppPermissionsMiddleware` will not work. For more information, see [Reversing namespaced URLs](https://docs.djangoproject.com/en/dev/topics/http/urls/#reversing-namespaced-urls).
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
